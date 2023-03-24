from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user_app.models import User


class UserAdmin(BaseUserAdmin):
    """Organises how the User information is displayed on the admin site."""
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


# Adds the User model to the admin page
admin.site.register(User, UserAdmin)