from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import TopicViewSet, TaskViewSet

app_name = 'topics'

router = DefaultRouter()
router.register('topics', TopicViewSet)
router.register('tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls))
]
