from django.shortcuts import render, get_object_or_404, redirect
from .models import Checklist, ChecklistItem


"""Renders a view of the checklist with the corresponding id.

Parameters
----------
checklist_id: int
    The id of the checklist
"""
def checklist_view(request, checklist_id):
    checklist = get_object_or_404(Checklist, pk=checklist_id)
    return render(request, 'cl_app/checklist.html', {'checklist': checklist})

"""Updates the status of a given checklist item.

Parameters
----------
checklist_id: int
    The id of the checklist that has the item
checklistitem_id: int
    The id of the checklist item
value: int
    An int indictating the status that the given item needs to be updated to.
"""
def update_item_status(request, checklist_id, checklistitem_id, value):
    checklist_item = get_object_or_404(ChecklistItem, pk=checklistitem_id)
    checklist_item.item_status = value
    checklist_item.save()
    return redirect('cl_app:checklist', checklist_id=checklist_id)