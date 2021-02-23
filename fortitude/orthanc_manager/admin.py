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
            )
        }),
    )
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(OrthancServer, OrthancServerAdmin)
