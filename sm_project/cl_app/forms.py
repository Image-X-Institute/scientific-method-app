from django import forms
from .models import Checklist, ChecklistItem
from ..user_app.models import User


class ChecklistForm(forms.ModelForm):

    class Meta:
        model = Checklist
        fields = ['checklist_title', 'researchers', 'reviewers']

    checklist_title = forms.CharField(label="Checklist Title")
    checklist_users = forms.ModelMultipleChoiceField(
        label="Checklist Users",
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    researchers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    reviewers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class ChecklistItemForm(forms.ModelForm):

    class Meta:
        model = ChecklistItem
        fields = ['item_title']
    
    item_title = forms.CharField(label="Add Item")
