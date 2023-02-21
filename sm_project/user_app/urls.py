from django.urls import path
from . import views


app_name = 'user_app'
# The urls that are a part of the app, "user_app"
urlpatterns = [
    path("", views.login_request, name="login"),
]