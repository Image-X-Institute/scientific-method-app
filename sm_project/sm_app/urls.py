from django.urls import path

from . import views

app_name = 'sm_app'
urlpatterns = [
    path('<int:checklist_id>/', views.checklist_view, name='checklist'),
]