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

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChecklistForm, self).__init__(*args, **kwargs)

    def clean(self):
        researchers = self.cleaned_data['researchers']
        reviewers = self.cleaned_data['reviewers']

        if self.user not in researchers and self.user not in reviewers:
            raise forms.ValidationError("Please include the creator of the checklist in either researchers or reviewers.")
            
            


class ChecklistItemForm(forms.ModelForm):

    class Meta:
        model = ChecklistItem
        fields = ['item_title']
    
    item_title = forms.CharField(label="Add Item")
