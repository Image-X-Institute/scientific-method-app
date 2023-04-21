from django.apps import AppConfig


class UserAppConfig(AppConfig):
    """Creates a path to add to INSTALLED_APPS in settings.py."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sm_project.user_app'
