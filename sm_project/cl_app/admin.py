from django.contrib import admin
from .forms import ChecklistAdminForm
from .models import Checklist, ChecklistItem


class UserFilter(admin.SimpleListFilter):
    """ Creates a list filter that filters by specific users and displays which both the user's name and email. """
    title = 'User'
    parameter_name = 'user'

    def lookups(self, request, model_admin):
        users = set()
        for user_sets in model_admin.model.objects.all():
            for user in user_sets.checklist_users.all():
                users.add(user)
        return [(user.id, (user.name + " - " + user.email)) for user in users]
    
    def queryset(self, request, queryset):
        if self.value() == None:
            return queryset.all()
        else:
            return queryset.filter(checklist_users__id = self.value())

class ChecklistAdmin(admin.ModelAdmin):
    """ Organises how the information about each checklist is displayed on the admin site. """
    fieldsets = (
        (None, {
        'fields': ('checklist_title', 'creator', 'checklist_users', 'researchers', 'reviewers')
        }),
    )
    readonly_fields = ['checklist_users']
    list_display = ['checklist_title', 'creator_name']
    list_filter = [UserFilter]
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
        'fields': ('item_title', 'item_checklist', 'item_status', 'estimate')
        }),
    )
    list_display = ['item_title', 'item_checklist', 'item_status', 'estimate']
    list_filter = ['item_status', 'item_checklist']
    search_fields = ['item_title']
    ordering = ['item_checklist', 'item_title']


# Adds the Checklist and ChecklistItem models to the admin page
admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(ChecklistItem, ChecklistItemAdmin)