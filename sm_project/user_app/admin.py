from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password')}),
        ('Permissions', {'fields': ('admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2')
        }),
    )
    list_display = ['name', 'email', 'admin']
    list_filter = ['admin']
    search_fields = ['name', 'email']
    ordering = ['name', 'email']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)