from django.test import TestCase

from sm_project.cl_app.models import Checklist
from sm_project.user_app.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_superuser("user1@test.com", "Test User 1", "test1")
        cls.user2 = User.objects.create_user("user2@test.com", "Test User 2", "test2")
        cls.test1 = Checklist.objects.create(checklist_title=f"Temp{cls.user1.id}", creator=cls.user1)
    
    def test__str__(self):
        self.assertEqual(self.user1.__str__(), "Test User 1 - user1@test.com")
        self.assertEqual(self.user2.__str__(), "Test User 2 - user2@test.com")

    def test_is_staff(self):
        self.assertTrue(self.user1.is_staff)

    def test_is_admin(self):
        self.assertTrue(self.user1.is_admin)

    def test_has_temp_checklist(self):
        self.assertTrue(self.user1.has_temp_checklist())
        self.assertFalse(self.user2.has_temp_checklist())

    def test_get_temp_checklist(self):
        self.assertEqual(self.user1.get_temp_checklist(), self.test1)

