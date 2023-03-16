from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Checklist, ChecklistItem
from .forms import ChecklistForm, ChecklistItemForm


@login_required(login_url='user_app:login')
def checklist_index(request):
    """Renders a view of all the checklists that the user has."""
    if request.user.has_temp_checklist():
        request.user.get_temp_checklist().delete()
    return render(request, 'cl_app/checklist_index.html', {'user_checklists': request.user})
    
@login_required(login_url='user_app:login')
def add_checklist(request):
    """Renders a view of the add checklist screen and allows the user to create a new checklist."""
    item_form = ChecklistItemForm()
    if request.user.has_temp_checklist():
        temp_checklist = request.user.get_temp_checklist()
    else:
        temp_checklist = Checklist(checklist_title = (f"Temp{request.user.id}"), creator = request.user)
        temp_checklist.save()
    if request.method == "POST":
        checklist_form = ChecklistForm(data=request.POST, initial={'creator': request.user})
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
        checklist_form = ChecklistForm(initial={'creator': request.user})
    return render(
        request, 
        'cl_app/add_checklist.html', 
        {'checklist_form': checklist_form, 'item_form': item_form, 'temp_checklist': temp_checklist}
    )

@login_required(login_url='user_app:login')
def add_temp_item(request):
    """Adds an item to a checklist that is used to store the checklist items until the user finalises the details of the checklist."""
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

@login_required(login_url='user_app:login')
def remove_temp_item(request, item_id):
    """Removes an item from the temporary storage checklist.

    Parameters
    ----------
    item_id: int
        The id of the temporary checklist item.
    """
    item = get_object_or_404(ChecklistItem, pk=item_id)
    item_checklist = request.user.get_temp_checklist()
    if item.item_checklist == item_checklist:
        item.delete()
    return redirect('cl_app:add_checklist')

@login_required(login_url='user_app:login')
def leave_checklist(request, checklist_id):
    """Allows the user to remove themselves from a checklist's list of users.

    Parameters
    ----------
    checklist_id: int
        The id of the checklist that the user is leaving
    """
    checklist = get_object_or_404(Checklist, pk=checklist_id)
    if checklist.creator != request.user and checklist.checklist_users.contains(request.user):
        checklist.checklist_users.remove(request.user)
        if checklist.researchers.contains(request.user):
            checklist.researchers.remove(request.user)
        if checklist.reviewers.contains(request.user):
            checklist.reviewers.remove(request.user)
    return redirect('cl_app:user_checklists')

@login_required(login_url='user_app:login')
def remove_checklist(request, checklist_id):
    """Allows the creator of a checklist to delete said checklist.

    Parameters
    ----------
    checklist_id: int
        The id of the checklist
    """
    checklist = get_object_or_404(Checklist, pk=checklist_id)
    if checklist.creator == request.user:
        checklist.delete()
    return redirect('cl_app:user_checklists')

@login_required(login_url='user_app:login')
def checklist_view(request, checklist_id):
    """Renders a view of the checklist with the corresponding id.

    Parameters
    ----------
    checklist_id: int
        The id of the checklist
    """
    checklist = get_object_or_404(Checklist, pk=checklist_id)
    if checklist.checklist_users.contains(request.user):
        return render(request, 'cl_app/checklist.html', {'checklist': checklist})
    else:
        return redirect('cl_app:user_checklists')
    
@login_required(login_url='user_app:login')
def open_document(request, checklist_id):
    """Opens the document associated with the checklist in a new tab.

    Parameters
    ----------
    checklist_id: int
        The id of the checklist
    """
    checklist = get_object_or_404(Checklist, pk=checklist_id)
    if checklist.checklist_users.contains(request.user):
        return redirect(checklist.document)
    else:
        return redirect('cl_app:user_checklists')

@login_required(login_url='user_app:login')
def update_item_status(request, checklist_id, checklistitem_id, value):
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
    checklist = get_object_or_404(Checklist, pk=checklist_id)
    if (checklist.researchers.contains(request.user) and value == 2) or \
        (checklist.reviewers.contains(request.user) and (value == 1 or value == 3)):
        checklist_item = get_object_or_404(ChecklistItem, pk=checklistitem_id)
        checklist_item.item_status = value
        checklist_item.save()
        return redirect('cl_app:checklist', checklist_id=checklist_id)
    else:
        return redirect('cl_app:user_checklists')

@login_required(login_url='user_app:login')
def edit_checklist(request, checklist_id):
    """Renders a view of the edit_checklist page. 
    Upon submission of the form, the checklist will be updated with the new information.

    Parameters
    ----------
    checklist_id: int
        The id of the checklist that's being edited.
    """
    checklist = get_object_or_404(Checklist, pk=checklist_id)
    if checklist.checklist_users.contains(request.user):
        item_form = ChecklistItemForm()
        if request.method == "POST":
            checklist_form = ChecklistForm(data=request.POST, initial={'creator': request.user})
            if checklist_form.is_valid():
                checklist.checklist_title = checklist_form.cleaned_data.get('checklist_title')
                checklist.researchers.set(checklist_form.cleaned_data.get('researchers'))
                checklist.reviewers.set(checklist_form.cleaned_data.get('reviewers'))
                checklist.checklist_users.set(checklist.researchers.all().union(checklist.reviewers.all()))
                checklist.save()
                return redirect('cl_app:checklist', checklist.id)
        else:
            checklist_form = ChecklistForm(initial={
                'checklist_title': checklist.checklist_title, 
                'creator': request.user,
                'researchers': [researcher.id for researcher in checklist.researchers.all()], 
                'reviewers': [reviewer.id for reviewer in checklist.reviewers.all()], 
            })
        return render(
            request, 
            'cl_app/edit_checklist.html', 
            {'checklist': checklist, 'checklist_form': checklist_form, 'item_form': item_form},
        )
    else:
        return redirect('cl_app:user_checklists')

@login_required(login_url='user_app:login')
def add_item(request, checklist_id):
    """Adds a checklist item to the checklist with the corresponding id.

    Parameters
    ----------
    checklist_id: int
        The id of the checklist
    """  
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
        return redirect('cl_app:edit_checklist', checklist_id)
    else:
        return redirect('cl_app:user_checklists')

@login_required(login_url='user_app:login')
def remove_item(request, checklistitem_id):
    """Removes a checklist item of the checklist with the corresponding id.

    Parameters
    ----------
    checklist_id: int
        The id of the checklist
    """  
    item = get_object_or_404(ChecklistItem, pk=checklistitem_id)
    if item.item_checklist.checklist_users.contains(request.user):
        item.delete()
        return redirect('cl_app:edit_checklist', item.item_checklist.pk)
    else:
        return redirect('cl_app:user_checklists')
