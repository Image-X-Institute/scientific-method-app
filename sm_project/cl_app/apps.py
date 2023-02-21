from django.apps import AppConfig


# Creates a path to add to INSTALLED_APPS in settings.py.
class ClAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sm_project.cl_app'
