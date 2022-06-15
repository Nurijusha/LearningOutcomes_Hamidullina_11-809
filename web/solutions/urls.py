from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import (SolutionViewSet, SolutionTestingCreateAPIView,
                       SolutionTestingRetrieveAPIView)

app_name = 'solutions'

router = DefaultRouter()
router.register('solutions', SolutionViewSet, basename='solutions')

urlpatterns = [
    path('', include(router.urls)),
    path('solution-testing/', SolutionTestingCreateAPIView.as_view(),
         name='Create SolutionTesting'),
    path('solution-testing/<int:id>/',
         SolutionTestingRetrieveAPIView.as_view(),
         name='Retrieve info about SolutionTesting')

]
