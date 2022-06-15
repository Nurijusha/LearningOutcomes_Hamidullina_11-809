from django.contrib import admin

from .models import Topic, Task


class TaskInline(admin.TabularInline):
    fk_name = 'topic'
    model = Task


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'name')
    list_display_links = ('name',)
    list_filter = ('number', 'name')
    inlines = [TaskInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'name', 'description')
    list_display_links = ('name',)
    list_filter = ('number', 'name')
