from django.conf import settings
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


app_name = 'cl_app'
# The urls that are a part of the app, "cl_app"
urlpatterns = [
    path('', views.checklist_index, name="user_checklists"),
    path('add_checklist/', views.add_checklist, name="add_checklist"),
    path('add_checklist/add_item/', views.add_temp_item, name="add_temp_item"),
    path('add_checklist/remove_item<int:item_id>/', views.remove_temp_item, name="remove_temp_item"),
    path('leave_checklist<int:checklist_id>/', views.leave_checklist, name="leave_checklist"),
    path('remove_checklist<int:checklist_id>/', views.remove_checklist, name="remove_checklist"),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name="logout"),
    path('checklist<int:checklist_id>/', views.checklist_view, name="checklist"),
    path('checklist<int:checklist_id>/document/', views.open_document, name="open_document"),
    path('item<int:item_id>/update/', views.update_item_status, name="update_item_status"),
    path('checklist<int:checklist_id>/edit/', views.edit_checklist, name="edit_checklist"),
    path('checklist<int:checklist_id>/add/', views.add_item, name="add_item"),
    path('remove_item<int:checklistitem_id>/', views.remove_item, name="remove_item"),
]