from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import User, Checklist, ChecklistItem

def checklist_view(request, checklist_id):
    checklist = get_object_or_404(Checklist, pk=checklist_id)
    return render(request, 'sm_app/checklist.html', {'checklist': checklist})