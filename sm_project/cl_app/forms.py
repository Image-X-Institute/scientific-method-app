from django import forms
from .models import Checklist, ChecklistItem
from ..user_app.models import User


class ChecklistForm(forms.ModelForm):
    """Organises how the Checklist creation form will be set up"""
    class Meta:
        model = Checklist
        fields = ['checklist_title', 'creator', 'checklist_users', 'researchers', 'reviewers']

    checklist_title = forms.CharField(label="Checklist Title")
    creator = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.HiddenInput(),
    )
    checklist_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.MultipleHiddenInput(),
        required=False,
    )
    researchers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    reviewers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    def clean(self):
        cleaned_data = super(ChecklistForm, self).clean()
        researchers = cleaned_data.get('researchers')
        reviewers = cleaned_data.get('reviewers')
        user = cleaned_data.get('creator')

        if researchers and reviewers and user:
            if user not in researchers and user not in reviewers:
                raise forms.ValidationError("Please include the creator of the checklist in either researchers or reviewers.")
        return self.cleaned_data
    
class ChecklistAdminForm(ChecklistForm):
    """Organises how the Checklist creation form on the admin page will be set up"""

    creator = forms.ModelChoiceField(
        label="Creator Email", 
        queryset=User.objects.all(),
    )

class ChecklistItemForm(forms.ModelForm):
    """Organises how the ChecklistItem creation form will be set up"""
    class Meta:
        model = ChecklistItem
        fields = ['item_title', 'time_estimate']
    
    item_title = forms.CharField(label="Item Title")
    time_estimate = forms.DateField(label="Estimated Completion Date", required=False, widget=forms.SelectDateWidget)
