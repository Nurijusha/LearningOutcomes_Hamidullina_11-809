import logging

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from .models import Solution, SolutionTesting
from .serializers import (SolutionSerializer, SolutionTestingSerializer,
                          SolutionTestingSuccessSerializer)
from . import tasks
from .validators import github_url_validator

logger = logging.getLogger(__name__)


class SolutionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return self.request.user.solutions.all()


class SolutionTestingCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=SolutionSerializer,
                         responses={
                             200: SolutionTestingSerializer(many=False),
                             400: SolutionTestingSerializer(many=False)})
    def post(self, request, format=None):
        """
        Create new solution for testing.
        If testing started -> 200.
        If testing of user is already started -> 400.
        """
        github_url = self.request.data.get('github_url')
        user = self.request.user
        # If exists testing from user, return it
        started_tasks = SolutionTesting.objects.filter(
            user=user,
            status__exact='STARTED'
        )
        if started_tasks.exists():
            task = started_tasks[0]
            serializer = SolutionTestingSerializer(task)
            return Response(
                data=serializer.data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate github_url
        try:
            github_url_validator(github_url)
        except ValidationError as e:
            return Response(
                {'error': e.message}
            )
        # Create Solution for user with github_url
        solution = Solution(author=user, github_url=github_url)
        solution.save()

        # Running dynamic testing and save celery task id
        dt_task = tasks.dynamic_testing.delay(github_url, solution.id)
        # Running static testing and save celery task id
        st_task = tasks.static_testing.delay(github_url, solution.id)

        # Create SolutionCeleryTask with dynamic and static tests
        solution_testing = SolutionTesting(
            solution=solution,
            user=user,
            dynamic_test_task_id=dt_task.id,
            static_test_task_id=st_task.id,
            status='STARTED'
        )
        solution_testing.save()
        st_serializer = SolutionTestingSerializer(solution_testing)
        return Response(
            data=st_serializer.data,
            status=status.HTTP_201_CREATED
        )


class SolutionTestingRetrieveAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={202: SolutionTestingSerializer(many=False),
                                    200: SolutionTestingSuccessSerializer(
                                        many=False)}
                         )
    def get(self, request, id):
        """
        Check status of testing by CeleryTaskSolution id.
        """
        solution_testing: SolutionTesting = get_object_or_404(
            SolutionTesting,
            id=id
        )

        """
        Если придется возвращать состояние каждого селери таска и ошибки.
        
        data = {'solution_testing_id': solution_testing_id}
        if celery_task.dynamic_test_task_id:
            task = AsyncResult(celery_task.dynamic_test_task_id)
            data['dynamic_tests_state'] = task.state
        if celery_task.static_test_task_id:
            task = AsyncResult(celery_task.static_test_task_id)
            if task.state in ('SUCCESS', 'STARTED'):
                data['static_tests_state'] = task.state
            else:
                data['static_tests_state'] = 'ERROR'

        # If all tests is success, send solution id
        if celery_task.status == 'SUCCESS':
            data['solution_id'] = celery_task.solution.id"""

        if solution_testing.status == 'STARTED':
            serializer_class = SolutionTestingSerializer
            status_code = status.HTTP_202_ACCEPTED
        elif solution_testing.status == 'SUCCESS':
            serializer_class = SolutionTestingSuccessSerializer
            status_code = status.HTTP_200_OK
        else:
            data = {'error': 'Проверьте доступность github репозитория'}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = serializer_class(solution_testing)
        return Response(
            data=serializer.data,
            status=status_code,
        )
