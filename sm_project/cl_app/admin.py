from django.contrib import admin
from .models import Checklist, ChecklistItem


admin.site.register(Checklist)
admin.site.register(ChecklistItem)