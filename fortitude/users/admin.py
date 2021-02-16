from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'is_active', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User information', {'fields': ('username', 'last_login', 'is_active')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
