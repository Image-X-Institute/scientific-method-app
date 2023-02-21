from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_protect
from .models import User
from django.contrib.auth.forms import AuthenticationForm


@csrf_protect
def login_request(request):
    if request.method == "POST":
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {email}.")
                return redirect('cl_app:checklist', checklist_id=1)
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid form.")
    else:
        login_form = AuthenticationForm()
    return render(request, "user_app/login.html", {"login_form": login_form})