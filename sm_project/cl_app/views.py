from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from .models import User, Checklist, ChecklistItem

def checklist_view(request, checklist_id):
    checklist = get_object_or_404(Checklist, pk=checklist_id)
    return render(request, 'cl_app/checklist.html', {'checklist': checklist})

def update_item_status(request, checklist_id, checklistitem_id, value):
    checklist_item = get_object_or_404(ChecklistItem, pk=checklistitem_id)
    checklist_item.item_status = value
    checklist_item.save()
    return redirect('cl_app:checklist', checklist_id=checklist_id)