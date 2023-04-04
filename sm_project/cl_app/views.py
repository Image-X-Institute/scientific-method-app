from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect

from sm_project.cl_app.forms import ChecklistForm, ChecklistItemForm, FeedbackForm
from sm_project.cl_app.models import Checklist, ChecklistItem
from sm_project.settings import EMAIL_HOST_USER


@login_required(login_url='user_app:login')
def checklist_index(request):
    """Renders a view of all the checklists that the user has."""
    if request.user.has_temp_checklist():
        request.user.get_temp_checklist().delete()
    return render(request, 'cl_app/checklist_index.html', {'user_checklists': request.user})
    
@login_required(login_url='user_app:login')
def add_checklist(request):
    """Renders a view of the add checklist screen and allows the user to create a new checklist."""
    if request.user.has_temp_checklist():
        temp_checklist = request.user.get_temp_checklist()
    else:
        temp_checklist = Checklist(checklist_title = (f"Temp{request.user.id}"), creator = request.user)
        temp_checklist.save()
    item_form = ChecklistItemForm(item_checklist=temp_checklist)
    if request.method == "POST":
        checklist_form = ChecklistForm(data=request.POST, initial={'creator': request.user})
        if checklist_form.is_valid():
            new_checklist = Checklist(
                checklist_title = checklist_form.cleaned_data.get('checklist_title'), 
                document = checklist_form.cleaned_data.get('document'),
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
        item_form = ChecklistItemForm(request.POST, item_checklist=temp_checklist)
        if item_form.is_valid():
            new_item = ChecklistItem(
                item_checklist = temp_checklist,
                item_title = item_form.cleaned_data.get('item_title'),
                time_estimate = item_form.cleaned_data.get('time_estimate')
            )
            new_item.save()
            new_item.dependencies.set(item_form.cleaned_data.get('dependencies'))
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
def update_item_status(request, item_id):
    """Updates the status of a given checklist item.
    If the status is updated to 'For Review' and a email host has been set, an email is sent notifying the reviewers
    that a review has requested.
    If the status is updated to 'Incomplete', the user will be redirected to a form to provide feedback with.

    Parameters
    ----------
    item_id: int
        The id of the checklist item whose status will be updated.
    """
    item = get_object_or_404(ChecklistItem, pk=item_id)
    checklist = item.item_checklist
    value = int(request.POST.get("status"))
    if (checklist.researchers.contains(request.user) and value == 2) or \
        (checklist.reviewers.contains(request.user) and (value == 1 or value == 3)):
        item.item_status = value
        item.save()
        if value == 2 and EMAIL_HOST_USER != '':
            subject=f"Review Requested for {item.item_title} in {checklist.checklist_title}"
            message=f"{request.user.name} has requested that \"{item.item_title}\" as part of the checklist," +\
                f"\"{checklist.checklist_title}\" be peer reviewed by a reviewer. Login to the checklist webapp for more." 
            if checklist.document != "":
                message += f"\n\nFind the associated document at {checklist.document}"
            send_mail(subject, message, EMAIL_HOST_USER, checklist.reviewer_emails())
        elif value == 3 and EMAIL_HOST_USER != '':
            return redirect('cl_app:send_feedback', item_id=item_id)
        return redirect('cl_app:checklist', checklist_id=checklist.id)
    else:
        return redirect('cl_app:user_checklists')
    
@login_required(login_url='user_app:login')
def send_feedback(request, item_id):
    """Renders a view of the feedback page.
    Upon submission of the form, an email featuring the reviewer's feedback will be sent to the researchers.

    Parameters
    ----------
    item_id: int
        The id of the checklist item whose status will be updated.
    """
    item = get_object_or_404(ChecklistItem, pk=item_id)
    checklist = item.item_checklist
    if checklist.reviewers.contains(request.user):
        if request.method == "POST":
            feedback_form = FeedbackForm(request.POST)
            if feedback_form.is_valid():
                subject = f"Feedback regarding {item.item_title} in {checklist.checklist_title}"
                message = f"{request.user.name} has reviewed \"{item.item_title}\" as part of the checklist, " +\
                    f"\"{checklist.checklist_title}\"and provided the following feedback: " +\
                    f"\n\n{feedback_form.cleaned_data.get('feedback')}"
                if checklist.document != "":
                    message += f"\n\nFind the associated document at {checklist.document}"
                send_mail(subject, message, EMAIL_HOST_USER, checklist.researcher_emails())
                return redirect('cl_app:checklist', checklist_id=checklist.id)
        else:
            feedback_form = FeedbackForm()
        return render(request, 'cl_app/feedback.html', {'item': item, 'feedback_form': feedback_form})
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
        item_form = ChecklistItemForm(item_checklist=checklist)
        if request.method == "POST":
            checklist_form = ChecklistForm(data=request.POST, initial={'creator': checklist.creator})
            if checklist_form.is_valid():
                checklist.checklist_title = checklist_form.cleaned_data.get('checklist_title')
                checklist.document = checklist_form.cleaned_data.get('document')
                checklist.researchers.set(checklist_form.cleaned_data.get('researchers'))
                checklist.reviewers.set(checklist_form.cleaned_data.get('reviewers'))
                checklist.checklist_users.set(checklist.researchers.all().union(checklist.reviewers.all()))
                checklist.save()
                return redirect('cl_app:checklist', checklist.id)
        else:
            checklist_form = ChecklistForm(initial={
                'checklist_title': checklist.checklist_title, 
                'document': checklist.document,
                'creator': checklist.creator,
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
            item_form = ChecklistItemForm(request.POST, item_checklist=checklist)
            if item_form.is_valid():
                new_item = ChecklistItem(
                    item_checklist = checklist,
                    item_title = item_form.cleaned_data.get('item_title'),
                    time_estimate = item_form.cleaned_data.get('time_estimate')
                )
                new_item.save()
                new_item.dependencies.set(item_form.cleaned_data.get('dependencies'))
                item_form = ChecklistItemForm(item_checklist=checklist)
        else:
            item_form = ChecklistItemForm(item_checklist=checklist)
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
