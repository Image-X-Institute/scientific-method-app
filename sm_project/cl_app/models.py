from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL

class Checklist(models.Model):
    checklist_title = models.CharField(max_length=200)
    checklist_users = models.ManyToManyField(User)

    def __str__(self):
        return self.checklist_title

class ChecklistItem(models.Model):
    class Status(models.IntegerChoices):
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
