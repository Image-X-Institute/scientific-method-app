from django.shortcuts import render, get_object_or_404, redirect
from .models import Checklist, ChecklistItem


# Renders a view of all the checklists that the user has.
def checklist_index(request):
    if request.user.is_authenticated:
        return render(request, 'cl_app/checklist_index.html', {'user_checklists': request.user})
    else:
        return redirect('user_app:login')

def remove_checklist(request, checklist_id):
    if request.user.is_authenticated:
        checklist = get_object_or_404(Checklist, pk=checklist_id)
        if checklist.creator == request.user:
            checklist.delete()
        return redirect('cl_app:user_checklists')
    else:
        return redirect('user_app:login')

"""Renders a view of the checklist with the corresponding id.

Parameters
----------
checklist_id: int
    The id of the checklist
"""
def checklist_view(request, checklist_id):
    if request.user.is_authenticated:
        checklist = get_object_or_404(Checklist, pk=checklist_id)
        if checklist.checklist_users.contains(request.user):
            return render(request, 'cl_app/checklist.html', {'checklist': checklist})
        else:
            return redirect('cl_app:user_checklists')
    else:
        return redirect('user_app:login')

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
    if request.user.is_authenticated:
        checklist = get_object_or_404(Checklist, pk=checklist_id)
        if (checklist.researchers.contains(request.user) and value == 2) or \
            (checklist.reviewers.contains(request.user) and (value == 1 or value == 3)):
            checklist_item = get_object_or_404(ChecklistItem, pk=checklistitem_id)
            checklist_item.item_status = value
            checklist_item.save()
            return redirect('cl_app:checklist', checklist_id=checklist_id)
        else:
            return redirect('cl_app:user_checklists')
    else:
        return redirect('user_app:login')