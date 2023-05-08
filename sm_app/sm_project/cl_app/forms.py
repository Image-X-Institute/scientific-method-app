from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Hidden, Layout, Submit
from django import forms
from django.urls import reverse

from sm_project.cl_app.models import Checklist, ChecklistItem
from sm_project.user_app.models import User


class ChecklistForm(forms.ModelForm):
    """Organises how the Checklist creation form will be set up"""
    class Meta:
        model = Checklist
        fields = ['checklist_title', 'document', 'creator', 'checklist_users', 'researchers', 'reviewers']

    checklist_title = forms.CharField(label="Checklist Title")
    document = forms.URLField(label="Document Link", required=False)
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

    def __init__(self, *args, **kwargs):
        super(ChecklistForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('cl_app:add_checklist')
        self.helper.form_id = 'add_checklist'
        self.helper.label_class = 'col-lg-2 py-2'
        self.helper.field_class = 'col-lg-10 py-2'

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
        fields = ['item_title', 'time_estimate', 'dependencies']
    
    item_title = forms.CharField(label="Item Title")
    time_estimate = forms.DateField(
        label="Estimated Completion Date", 
        required=False, 
        widget=forms.SelectDateWidget(attrs=({'style': 'width: 32%; display: inline-block; margin-right: 6px; margin-left: 6px;'}))
    )
    dependencies = forms.ModelMultipleChoiceField(
        queryset=ChecklistItem.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        item_checklist = kwargs.pop('item_checklist', None)
        super(ChecklistItemForm, self).__init__(*args, **kwargs)
        if item_checklist != None:
            self.fields['dependencies'].queryset = ChecklistItem.objects.filter(item_checklist=item_checklist)
        else:
            self.fields['dependencies'].initial = self.instance.dependencies.all().values_list('id', flat=True)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('cl_app:add_temp_item')
        self.helper.label_class = 'col-lg-2 py-2'
        self.helper.field_class = 'col-lg-10 py-2'
        self.helper.layout = Layout(
            Field('item_title'),
            Field('time_estimate', css_class="text-center"),
            InlineCheckboxes('dependencies'),
            Submit('submit', 'Add Item', css_class="btn btn-success"),
        )
    
    def save(self, *args, **kwargs):
        instance = super(ChecklistItemForm, self).save(*args, **kwargs)
        instance.dependencies.set(self.cleaned_data['dependencies'])
        return instance

class ChecklistItemAdminForm(ChecklistItemForm):
    """Organises how the ChecklistItem creation form on the admin page will be set up"""
    class Meta:
        model = ChecklistItem
        fields = ['item_checklist', 'item_title', 'item_status', 'time_estimate', 'dependencies']
    
    def __init__(self, *args, **kwargs):
        super(ChecklistItemAdminForm, self).__init__(*args, **kwargs)
        dependencies = list()
        for item in ChecklistItem.objects.all():
            if self.instance in item.dependencies.all():
                dependencies.append(item.pk)
        dependencies.append(self.instance.pk)
        self.fields['dependencies'].queryset = ChecklistItem.objects.exclude(id__in=dependencies).filter(item_checklist=self.instance.item_checklist)
    
    def clean(self):
        cleaned_data = super(ChecklistItemAdminForm, self).clean()
        item_checklist = cleaned_data.get('item_checklist')
        dependencies = cleaned_data.get('dependencies')
        if dependencies and item_checklist:
            for dependency in dependencies:
                if dependency.item_checklist != item_checklist:
                    raise forms.ValidationError("All dependencies must belong to the same checklist.")
        return self.cleaned_data

class FeedbackForm(forms.Form):
    feedback = forms.CharField(label="", widget=forms.Textarea, max_length=2000)
    warning_override = forms.BooleanField(label="Warning Override", widget=forms.HiddenInput, initial=False, required=False)

    def clean_feedback(self):
        if len(self.cleaned_data["feedback"]) <= 30:
            raise forms.ValidationError("It's recommended that you provide feedback longer than 30 characters", "charactermin")
        else:
            return self.cleaned_data["feedback"]
