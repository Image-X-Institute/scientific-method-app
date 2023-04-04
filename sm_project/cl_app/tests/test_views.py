from django.test import TestCase
from django.urls import reverse

from sm_project.cl_app.models import Checklist, ChecklistItem
from sm_project.user_app.models import User


class ChecklistIndexTest(TestCase):
    def test_url_exists(self):
        response = self.client.get(reverse('cl_app:user_checklists'))
        self.assertTrue(response.status_code, 200)

class AddChecklistTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("user1@test.com", "Test User 1", "test1")
        self.user2 = User.objects.create_user("user2@test.com", "Test User 2", "test2")
        self.information = {
            'checklist_title': "Checklist Test",
            'creator': self.user1.pk,
            'researchers': [self.user2.pk],
            'reviewers': [self.user1.pk]
        }
    
    def test_add_checklist(self):
        self.client.login(username=self.user1.email, password='test1')
        response = self.client.post(reverse('cl_app:add_checklist'), self.information, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Checklist.objects.filter(checklist_title="Checklist Test").exists())
        self.assertRedirects(response, reverse('cl_app:user_checklists'))

class AddTempItemTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("user1@test.com", "Test User 1", "test1")
        self.temp_checklist = Checklist(checklist_title = (f"Temp{self.user.id}"), creator = self.user)
        self.temp_checklist.save()
        self.information = {'item_title': "Item Test"}
    
    def test_add_temp_item(self):
        self.client.login(username=self.user.email, password='test1')
        response = self.client.post(reverse('cl_app:add_temp_item'), self.information, follow=True)
        self.assertTrue(self.temp_checklist.checklistitem_set.filter(item_title="Item Test").exists())
        self.assertRedirects(response, reverse('cl_app:add_checklist'))

class RemoveTempItemTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("user1@test.com", "Test User 1", "test1")
        self.temp_checklist = Checklist(checklist_title = (f"Temp{self.user.id}"), creator = self.user)
        self.temp_checklist.save()
        self.item = ChecklistItem(item_checklist=self.temp_checklist, item_title="Item Test")
        self.item.save()
        self.information = {'item_title': "Item Test"}
    
    def test_add_temp_item(self):
        self.client.login(username=self.user.email, password='test1')
        response = self.client.post(reverse('cl_app:remove_temp_item', kwargs={'item_id': self.item.pk}), self.information, follow=True)
        self.assertFalse(self.temp_checklist.checklistitem_set.filter(item_title="Item Test").exists())
        self.assertRedirects(response, reverse('cl_app:add_checklist'))

class LeaveChecklistTest(TestCase):
    def setUp(self):
        return

class RemoveChecklistTest(TestCase):
    def setUp(self):
        return

class ChecklistViewTest(TestCase):
    def setUp(self):
        return

class OpenDocumentTest(TestCase):
    def setUp(self):
        return

class UpdateItemStatusTest(TestCase):
    def setUp(self):
        return

class SendFeedbackTest(TestCase):
    def setUp(self):
        return

class EditChecklistTest(TestCase):
    def setUp(self):
        return

class AddItemTest(TestCase):
    def setUp(self):
        return

class RemoveItemTest(TestCase):
    def setUp(self):
        return
