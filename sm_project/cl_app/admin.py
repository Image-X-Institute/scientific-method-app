from django.contrib import admin
from .models import Checklist, ChecklistItem


# Adds the Checklist and ChecklistItem models to the admin page
admin.site.register(Checklist)
admin.site.register(ChecklistItem)