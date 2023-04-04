from django.test import TestCase

from sm_project.cl_app.models import Checklist, ChecklistItem
from sm_project.user_app.models import User

class ChecklistModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user("user1@test.com", "Test User 1", "test1")
        cls.user2 = User.objects.create_user("user2@test.com", "Test User 2", "test2")
        cls.check1 = Checklist.objects.create(checklist_title="Checklist Test 1", creator=cls.user1)
        cls.check2 = Checklist.objects.create(checklist_title="Checklist Test 2", creator=cls.user2)
        cls.check1.researchers.add(cls.user1)
        cls.check1.reviewers.add(cls.user2)
        cls.check2.researchers.add(cls.user2)
        cls.check2.reviewers.add(cls.user1)
    
    def test__str__(self):
        self.assertEqual(self.check1.__str__(), "Checklist Test 1")
        self.assertEqual(self.check2.__str__(), "Checklist Test 2")
    
    def test_creator_name(self):
        self.assertEqual(self.check1.creator_name, "Test User 1")
        self.assertEqual(self.check2.creator_name, "Test User 2")
    
    def test_researcher_emails(self):
        self.assertEqual(self.check1.researcher_emails(), ["user1@test.com"])
        self.assertEqual(self.check2.researcher_emails(), ["user2@test.com"])
    
    def test_reviewer_emails(self):
        self.assertEqual(self.check1.reviewer_emails(), ["user2@test.com"])
        self.assertEqual(self.check2.reviewer_emails(), ["user1@test.com"])

class ChecklistItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("user1@test.com", "Test User", "test1")
        cls.check1 = Checklist.objects.create(checklist_title="Checklist Test 1", creator=cls.user)
        cls.check2 = Checklist.objects.create(checklist_title="Checklist Test 2", creator=cls.user)
        cls.item1_1 = ChecklistItem.objects.create(item_checklist=cls.check1, item_title="Item 1 - Checklist 1", item_status=2)
        cls.item2_1 = ChecklistItem.objects.create(item_checklist=cls.check1, item_title="Item 2 - Checklist 1", item_status=3)
        cls.item1_2 = ChecklistItem.objects.create(item_checklist=cls.check2, item_title="Item 1 - Checklist 2", item_status=1)
        cls.item2_2 = ChecklistItem.objects.create(item_checklist=cls.check2, item_title="Item 2 - Checklist 2", item_status=3)
        cls.item2_1.dependencies.add(cls.item1_1)
        cls.item2_1.dependencies.add(cls.item2_1)
        cls.item2_2.dependencies.add(cls.item1_2)
    
    def test__str__(self):
        self.assertEqual(self.item1_1.__str__(), "Item 1 - Checklist 1")
        self.assertEqual(self.item2_1.__str__(), "Item 2 - Checklist 1")
    
    def test_get_status(self):
        self.assertEqual(self.item1_1.get_status(), "For Review")
        self.assertEqual(self.item2_1.get_status(), "Incomplete")
        self.assertEqual(self.item1_2.get_status(), "Completed")

    def test_get_dependancies(self):
        self.assertEqual(self.item1_1.get_dependencies(), "")
        self.assertEqual(self.item2_1.get_dependencies(), " - Dependant On: Item 1 - Checklist 1, Item 2 - Checklist 1")
        self.assertEqual(self.item2_2.get_dependencies(), " - Dependant On: Item 1 - Checklist 2")
    
    def test_dependencies_completed(self):
        self.assertTrue(self.item1_1.dependencies_completed())
        self.assertFalse(self.item2_1.dependencies_completed())
        self.assertTrue(self.item2_2.dependencies_completed())
