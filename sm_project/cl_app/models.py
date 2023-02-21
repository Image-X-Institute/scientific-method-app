from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL

class Checklist(models.Model):
    """A model class used to represent the checklists.

    Attributes
    ----------
    checklist_title: CharField
        The title of the checklist.
    checklist_users: ManyToManyField
        A field that stores the many to many relationships between the checklists and the users.

    Methods
    -------
    __str__(self)
        Prints the title of the checklist
    """
    checklist_title = models.CharField(max_length=200)
    checklist_users = models.ManyToManyField(User)

    def __str__(self):
        return self.checklist_title

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
        IN_REVIEW = 2, 'In Review'
        INCOMPLETE = 3, 'Incomplete'

    item_checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    item_title = models.CharField(max_length=200)
    item_status = models.IntegerField(choices=Status.choices, default=Status.INCOMPLETE)

    def __str__(self):
        return self.item_title

    def get_status(self):
        return self.Status(self.item_status).label
