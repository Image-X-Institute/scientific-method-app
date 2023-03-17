from django.contrib import admin
from .forms import ChecklistAdminForm
from .models import Checklist, ChecklistItem


class ChecklistAdmin(admin.ModelAdmin):
    """ Organises how the information about each checklist is displayed on the admin site. """
    fieldsets = (
        (None, {
        'fields': ('checklist_title', 'document', 'creator', 'checklist_users', 'researchers', 'reviewers')
        }),
    )
    readonly_fields = ['checklist_users']
    list_display = ['checklist_title', 'creator_name']
    list_filter = ['checklist_users']
    search_fields = ['checklist_title', 'creator_name']
    ordering = ['checklist_title']
    form = ChecklistAdminForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.checklist_users.set(form.cleaned_data.get('researchers').union(form.cleaned_data.get('reviewers')))

class ChecklistItemAdmin(admin.ModelAdmin):
    """Organises how the information about each checklist item is displayed on the admin site."""
    fieldsets = (
        (None, {
        'fields': ('item_title', 'item_checklist', 'item_status', 'time_estimate')
        }),
    )
    list_display = ['item_title', 'item_checklist', 'item_status', 'time_estimate']
    list_filter = ['item_status', 'item_checklist']
    search_fields = ['item_title']
    ordering = ['item_checklist', 'item_title']


# Adds the Checklist and ChecklistItem models to the admin page
admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(ChecklistItem, ChecklistItemAdmin)