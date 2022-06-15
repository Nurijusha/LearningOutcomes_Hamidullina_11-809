from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_superuser')
    list_display_links = ('username',)
    list_filter = ('email', 'username')
    exclude = ('user_permissions', 'groups')
