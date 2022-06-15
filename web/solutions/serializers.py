import logging

from rest_framework import serializers

from .models import Solution, LearningOutcome, Recommendation, \
    SolutionTesting

logger = logging.getLogger(__name__)


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = ('name', 'task')


class LearningOutcomeSerializer(serializers.ModelSerializer):
    recommendations = RecommendationSerializer(read_only=True,
                                               many=True)

    class Meta:
        model = LearningOutcome
        fields = ('name', 'score', 'recommendations')


class SolutionSerializer(serializers.ModelSerializer):
    learning_outcomes = LearningOutcomeSerializer(read_only=True,
                                                  many=True)

    class Meta:
        model = Solution
        fields = ('id', 'created_at', 'github_url', 'learning_outcomes')


class SolutionTestingSerializer(serializers.ModelSerializer):

    class Meta:
        model = SolutionTesting
        """
        Если надо будет возвращать результат по каждому селери таску
        fields = ('solution_testing_id', 'created_at',
                  'dynamic_test_task_id', 'static_test_task_id', 'status')"""
        fields = ('id', 'created_at', 'status')


class SolutionTestingSuccessSerializer(serializers.ModelSerializer):
    solution_id = serializers.IntegerField(source='solution.id',
                                           read_only=True)

    class Meta:
        model = SolutionTesting
        fields = ('id', 'created_at', 'status', 'solution_id')
