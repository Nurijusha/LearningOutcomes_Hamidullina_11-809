from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.timezone import localtime

from users.models import User
import solutions.validators as custom_validators


class Solution(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='solutions',
        verbose_name='Автор решения',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    github_url = models.CharField(
        max_length=200,
        validators=[custom_validators.github_url_validator],
        verbose_name='URL GitHub репозитория',
    )

    def get_created_at_in_str(self):
        return localtime(self.created_at).strftime('%Y.%m.%d %H:%M')

    def __str__(self):
        return f'{self.author.username} {self.get_created_at_in_str()}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Решение'
        verbose_name_plural = 'Решения'


class Recommendation(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Необходимо повторить или изучить',
    )
    task = models.CharField(
        max_length=50,
        verbose_name='Номер задачи для повторения',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рекомендация'
        verbose_name_plural = 'Рекомендации'


class LearningOutcome(models.Model):
    solution = models.ForeignKey(
        Solution,
        on_delete=models.CASCADE,
        related_name='learning_outcomes',
        verbose_name='Решение',
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название образовательного результата',
    )
    score = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5)],
        verbose_name='Уровень'
    )
    recommendations = models.ManyToManyField(
        Recommendation,
        related_name='learning_outcomes',
        verbose_name='Рекомендации к образовательному результату решения'
    )

    def __str__(self):
        return f'{self.name} - score {self.score}'

    class Meta:
        verbose_name = 'Образовательный результат решения'
        verbose_name_plural = 'Образовательные результаты решений'


class SolutionTesting(models.Model):
    solution = models.OneToOneField(
        Solution,
        on_delete=models.SET_NULL,
        related_name='celery_task',
        verbose_name='Решение',
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='celery_tasks',
        verbose_name='Автор',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    dynamic_test_task_id = models.CharField(
        max_length=100,
        verbose_name='ID задачи динамического тестирования',
    )
    static_test_task_id = models.CharField(
        max_length=100,
        verbose_name='ID задачи статического тестирования',
    )
    status = models.CharField(
        max_length=20,
        verbose_name='Статус выполнения задач'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Задача Celery на тестирование'
        verbose_name_plural = 'Задачи Celery на тестирования'
