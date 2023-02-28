from django import forms
from .models import Checklist
from ..user_app.models import User


class ChecklistForm(forms.ModelForm):

    class Meta:
        model = Checklist
        fields = ['checklist_title', 'researchers', 'reviewers']

    checklist_title = forms.CharField()
    researchers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    reviewers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
