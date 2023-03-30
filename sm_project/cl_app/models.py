from django.conf import settings
from django.contrib import admin
from django.db import models


User = settings.AUTH_USER_MODEL

class Checklist(models.Model):
    """A model class used to represent the checklists.

    Attributes
    ----------
    checklist_title: CharField
        The title of the checklist.
    document: URLField
        The link to the document the checklist is attributed to.
        This attribute is optional.
    creator: ForeignKey
        The creator of the checklist.
    checklist_users: ManyToManyField
        A field that stores the many to many relationships between the checklists and the users.
    researchers: ManyToManyField
        A field that stores the many to many relationships between the checklists and the researchers.
    reviewers: ManyToManyField
        A field that stores the many to many relationships between the checklists and the researchers.

    Methods
    -------
    __str__(self)
        Prints the title of the checklist
    creator_name(self):
        Returns the name of the creator of the checklist.
    """
    checklist_title = models.CharField(verbose_name="Checklist", max_length=200)
    document = models.URLField(verbose_name="Document Link", max_length=150, blank=True)
    creator = models.ForeignKey(User, verbose_name="Creator Email", on_delete=models.CASCADE, related_name='creator')
    checklist_users = models.ManyToManyField(User, verbose_name="Checklist Users")
    researchers = models.ManyToManyField(User, related_name='researchers')
    reviewers = models.ManyToManyField(User, related_name='reviewers', blank=True)

    def __str__(self):
        return self.checklist_title
    
    @property
    @admin.display(description="Creator")
    def creator_name(self):
        return self.creator.name
    
    def researcher_emails(self):
        email_list = list()
        for user in self.researchers.all():
            email_list.append(user.email)
        return email_list
    
    def reviewer_emails(self):
        email_list = list()
        for user in self.reviewers.all():
            email_list.append(user.email)
        return email_list

class ChecklistItem(models.Model):
    """A model class used to represent the items in each of the checklists.

    Attributes
    ----------
    item_checklist: ForeignKey
        The checklist that the checklist item is connected to.
    item_title: CharField
        The title of the checklist item
    item_status: IntegerField
       The status of an item as an integer. The available choices can be found in the class, Status.
       The default status is INCOMPLETE or 3.
    time_estimate: DateField
        The estimated date that the checklist item is expected to be marked as complete by.
        This attribute is optional.
    dependancies: ManyToManyField
        The items that the item is the dependant on being marked as completed before they can be requested for review.
        This attribute is optional.

    Methods
    -------
    __str__(self)
        Prints the title of the checklist item.
    get_status(self)
        Returns the status of the checklist item.
    """
    class Status(models.IntegerChoices):
        # A class that stores the available choices for the IntegerField, item_status
        COMPLETED = 1, 'Completed'
        FOR_REVIEW = 2, 'For Review'
        INCOMPLETE = 3, 'Incomplete'

    item_checklist = models.ForeignKey(Checklist, verbose_name="Checklist", on_delete=models.CASCADE)
    item_title = models.CharField(verbose_name="Checklist Item", max_length=200)
    item_status = models.IntegerField(verbose_name="Status", choices=Status.choices, default=Status.INCOMPLETE)
    time_estimate = models.DateField(verbose_name="Estimated Completion Date", null=True, blank=True)
    depending_items = models.ManyToManyField("self", related_name="dependancies", blank=True, symmetrical=False)

    def __str__(self):
        return self.item_title

    def get_status(self):
        return self.Status(self.item_status).label
