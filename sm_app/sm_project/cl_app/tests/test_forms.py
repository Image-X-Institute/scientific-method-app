import datetime

from django.test import TestCase

from sm_project.cl_app.forms import ChecklistForm, ChecklistItemForm, ChecklistItemAdminForm, FeedbackForm
from sm_project.cl_app.models import Checklist, ChecklistItem
from sm_project.user_app.models import User


class ChecklistFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user("user1@test.com", "Test User 1", "test1")
        cls.user2 = User.objects.create_user("user2@test.com", "Test User 2", "test2")
        cls.form1 = ChecklistForm(data={
            'checklist_title': "Checklist Test",
            'creator': cls.user1, 
            'checklist_users': [cls.user1, cls.user2],
            'researchers': [cls.user2], 
            'reviewers': [cls.user1]
        })
        cls.form2 = ChecklistForm(data=dict(cls.form1.data))
        cls.form2.data['checklist_users'] = [cls.user2]
        cls.form2.data['researchers'] = [cls.user2]
        cls.form2.data['reviewers'] = [cls.user2]
        cls.form3 = ChecklistForm()
    
    def test_form(self):
        self.assertTrue(self.form1.is_valid())
        self.assertFalse(self.form2.is_valid())
        self.assertFalse(self.form3.is_valid())

class ChecklistItemFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("user1@test.com", "Test User 1", "test1")
        cls.check = Checklist.objects.create(checklist_title="Checklist Test 1", creator=cls.user)
        cls.item = ChecklistItem.objects.create(item_checklist=cls.check, item_title="Item 1", item_status=2)
        cls.form1 = ChecklistItemForm(item_checklist=cls.check, data={
            'item_checklist': cls.check,
            'item_title': "Item Test",
            'item_estimate': datetime.date.today,
            'dependencies': [cls.item]
        })
        cls.form2 = ChecklistItemForm(item_checklist=cls.check)
    
    def test_form(self):
        self.assertTrue(self.form1.is_valid())
        self.assertFalse(self.form2.is_valid())

class ChecklistItemAdminFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("user1@test.com", "Test User", "test1")
        cls.check1 = Checklist.objects.create(checklist_title="Checklist Test 1", creator=cls.user)
        cls.check2 = Checklist.objects.create(checklist_title="Checklist Test 2", creator=cls.user)
        cls.item1 = ChecklistItem.objects.create(item_checklist=cls.check1, item_title="Item Test 1", item_status=2)
        cls.item2 = ChecklistItem.objects.create(item_checklist=cls.check1, item_title="Item Test 2", item_status=2)
        cls.form1 = ChecklistItemAdminForm(instance=cls.item2, data={
            'item_checklist': cls.check1,
            'item_title': "Form Test 1",
            'item_status': 3,
            'item_estimate': datetime.date.today,
            'dependencies': [cls.item1]
        })
        cls.form2 = ChecklistItemAdminForm(instance=cls.item2, data=dict(cls.form1.data))
        cls.form2.data['item_checklist'] = cls.check2
        cls.form3 = ChecklistItemAdminForm(instance=cls.item2)
    
    def test_form(self):
        self.assertTrue(self.form1.is_valid())
        self.assertFalse(self.form2.is_valid())
        self.assertFalse(self.form3.is_valid())

class FeedbackFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form1 = FeedbackForm(data={'feedback': "Feedback Test"})
        cls.form2 = FeedbackForm()
    
    def test_form(self):
        self.assertTrue(self.form1.is_valid())
        self.assertFalse(self.form2.is_valid())
