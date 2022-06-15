from django.contrib import admin

from .models import (Solution, LearningOutcome, Recommendation,
                     SolutionTesting)


class LearningOutcomeInline(admin.TabularInline):
    fk_name = 'solution'
    model = LearningOutcome
    extra = 1


class RecommendationInline(admin.TabularInline):
    model = LearningOutcome.recommendations.through
    extra = 1


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_at', 'github_url')
    inlines = [LearningOutcomeInline]


@admin.register(LearningOutcome)
class LearningOutcomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'solution', 'name', 'score')
    inlines = [RecommendationInline]
    exclude = ('recommendations',)


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'task')


@admin.register(SolutionTesting)
class SolutionTestingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'solution', 'created_at', 'status',
                    'dynamic_test_task_id', 'static_test_task_id')
