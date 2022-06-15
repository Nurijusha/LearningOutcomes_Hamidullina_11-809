from rest_framework import serializers

from .models import Topic, Task


class TaskTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'number', 'name']


class TopicSerializer(serializers.ModelSerializer):
    tasks = TaskTopicSerializer(many=True)

    class Meta:
        model = Topic
        fields = ['id', 'number', 'name', 'tasks']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'number', 'name', 'description']
