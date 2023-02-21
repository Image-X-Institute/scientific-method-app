from django.urls import path
from . import views


app_name = 'cl_app'
# The urls that are a part of the app, "cl_app"
urlpatterns = [
    path('update_item_status/<int:checklist_id>/<int:checklistitem_id>/<int:value>/', views.update_item_status, name="update_item_status"),
    path('<int:checklist_id>/', views.checklist_view, name="checklist"),
]