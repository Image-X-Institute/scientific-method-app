from django.shortcuts import render, get_object_or_404, redirect
from .models import Checklist, ChecklistItem
from .forms import ChecklistForm, ChecklistItemForm


# Renders a view of all the checklists that the user has.
def checklist_index(request):
    if request.user.is_authenticated:
        if request.user.has_temp_checklist():
            request.user.get_temp_checklist().delete()
        return render(request, 'cl_app/checklist_index.html', {'user_checklists': request.user})
    else:
        return redirect('user_app:login')
    
# Renders a view of the add checklist screen and allows the user to create a new checklist.
def add_checklist(request):
    if request.user.is_authenticated:
        item_form = ChecklistItemForm()
        if request.user.has_temp_checklist():
            temp_checklist = request.user.get_temp_checklist()
        else:
            temp_checklist = Checklist(checklist_title = ("Temp" + str(request.user.id)), creator = request.user)
            temp_checklist.save()
        if request.method == "POST":
            checklist_form = ChecklistForm(request.POST)
            if checklist_form.is_valid():
                new_checklist = Checklist(
                    checklist_title = checklist_form.cleaned_data.get('checklist_title'), 
                    creator = request.user
                )
                new_checklist.save()
                new_checklist.researchers.set(checklist_form.cleaned_data.get('researchers'))
                new_checklist.reviewers.set(checklist_form.cleaned_data.get('reviewers'))
                new_checklist.checklist_users.set(new_checklist.researchers.all().union(new_checklist.reviewers.all()))
                new_checklist.checklistitem_set.set(temp_checklist.checklistitem_set.all())
                temp_checklist.delete()
                return redirect('cl_app:user_checklists')
        else:
            checklist_form = ChecklistForm()
        return render(
            request, 
            'cl_app/add_checklist.html', 
            {'checklist_form': checklist_form, 'item_form': item_form, 'temp_checklist': temp_checklist}
        )
    else:
        return redirect('user_app:login')

def add_temp_item(request):
    if request.user.is_authenticated:
        temp_checklist = request.user.get_temp_checklist()
        if request.method == "POST":
            item_form = ChecklistItemForm(request.POST)
            if item_form.is_valid():
                new_item = ChecklistItem(
                    item_checklist = temp_checklist,
                    item_title = item_form.cleaned_data.get('item_title')
                )
                new_item.save()
        return redirect('cl_app:add_checklist')
    else:
        return redirect('user_app:login')

"""Allows the creator of a checklist to delete said checklist.

Parameters
----------
checklist_id: int
    The id of the checklist
"""
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
            item_form = ChecklistItemForm()
            return render(request, 'cl_app/checklist.html', {'checklist': checklist, 'item_form': item_form})
        else:
            return redirect('cl_app:user_checklists')
    else:
        return redirect('user_app:login')

"""Adds a checklist item to the checklist with the corresponding id.

Parameters
----------
checklist_id: int
    The id of the checklist
"""  
def add_item(request, checklist_id):
    if request.user.is_authenticated:
        checklist = get_object_or_404(Checklist, pk=checklist_id)
        if checklist.checklist_users.contains(request.user):
            if request.method == "POST":
                item_form = ChecklistItemForm(request.POST)
                if item_form.is_valid():
                    new_item = ChecklistItem(
                        item_checklist = checklist,
                        item_title = item_form.cleaned_data.get('item_title')
                    )
                    new_item.save()
                    item_form = ChecklistItemForm()
            else:
                item_form = ChecklistItemForm()
            return redirect('cl_app:checklist', checklist_id)
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