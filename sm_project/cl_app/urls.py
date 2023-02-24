from django.conf import settings
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


app_name = 'cl_app'
# The urls that are a part of the app, "cl_app"
urlpatterns = [
    path('', views.checklist_index, name="user_checklists"),
    path('checklist<int:checklist_id>/', views.checklist_view, name="checklist"),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name="logout"),
    path('update_item_status/<int:checklist_id>/<int:checklistitem_id>/<int:value>/', views.update_item_status, name="update_item_status"),
]