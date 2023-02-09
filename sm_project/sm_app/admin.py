from django.contrib import admin

from .models import User, Checklist

admin.site.register(User)
admin.site.register(Checklist)