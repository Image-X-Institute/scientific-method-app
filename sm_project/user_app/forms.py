from django.contrib.auth.forms import UserCreationForm

from sm_project.user_app.models import User


class NewUserForm(UserCreationForm):
    """Organises how the User creation form will be set up"""
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']