from django import forms
from .models import Checklist, ChecklistItem
from ..user_app.models import User


class ChecklistForm(forms.ModelForm):
    """Organises how the Checklist creation form will be set up"""
    class Meta:
        model = Checklist
        fields = ['checklist_title', 'document', 'researchers', 'reviewers']

    checklist_title = forms.CharField(label="Checklist Title")
    document = forms.URLField(label="Document Link", required=False)
    checklist_users = forms.ModelMultipleChoiceField(
        label="Checklist Users",
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
        if Checklist.objects.filter(id=self.instance.pk).exists():
            user = Checklist.objects.get(id=self.instance.pk).creator
        else:
            user = cleaned_data.get('creator')

        if researchers and reviewers:
            if user not in researchers and user not in reviewers:
                raise forms.ValidationError("Please include the creator of the checklist in either researchers or reviewers.")
        return self.cleaned_data

class ChecklistItemForm(forms.ModelForm):
    """Organises how the ChecklistItem creation form will be set up"""
    class Meta:
        model = ChecklistItem
        fields = ['item_title']
    
    item_title = forms.CharField(label="Add Item")
