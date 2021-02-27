from django.contrib import admin

from .models import OrthancServer


class OrthancServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    fieldsets = (
        ('Configuration', {
            'fields': (
                'name',
                'address',
                'has_credentials',
                'username',
                'password',
            ),
        }),
        ('Authorization', {
            'fields': (
                'is_restricted',
                'authorized_users',
            ),
        }),
    )
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('authorized_users',)


admin.site.register(OrthancServer, OrthancServerAdmin)
