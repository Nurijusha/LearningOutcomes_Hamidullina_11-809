from django.db import models


class Topic(models.Model):
    number = models.IntegerField(
        verbose_name='Номер',
        unique=True
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )

    class Meta:
        ordering = ['number']
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

    def __str__(self):
        return f'Модуль {self.number}. {self.name}'


class Task(models.Model):
    topic = models.ForeignKey(
        Topic,
        related_name='tasks',
        on_delete=models.CASCADE
    )
    number = models.IntegerField(verbose_name='Номер')
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    description = models.TextField(verbose_name='Описание')

    class Meta:
        ordering = ['topic', 'number']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f'Модуль {self.number}. {self.name}'
