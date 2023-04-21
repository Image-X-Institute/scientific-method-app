from django.test import TestCase
from django.urls import reverse

from sm_project.cl_app.models import Checklist
from sm_project.user_app.forms import NewUserForm
from sm_project.user_app.models import User


class NewUserFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form1 = NewUserForm(data={
            'name': "Test User",
            'email': "user1@test.com",
            'password1': "u0hN500N",
            'password2': "u0hN500N",
        })
        cls.form2 = NewUserForm(data=dict(cls.form1.data))
        cls.form2.data['password2'] = "0GB68jfg"
        cls.form3 = NewUserForm(data=dict(cls.form1.data))
        cls.form3.data['password1'] = "test1"
        cls.form3.data['password2'] = "test1"
        cls.form4 = NewUserForm()
    
    def test_form(self):
        self.assertTrue(self.form1.is_valid())
        self.assertFalse(self.form2.is_valid())
        self.assertFalse(self.form3.is_valid())
        self.assertFalse(self.form4.is_valid())

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_superuser("user1@test.com", "Test User 1", "test1")
        cls.user2 = User.objects.create_user("user2@test.com", "Test User 2", "test2")
        cls.check = Checklist.objects.create(checklist_title=f"Temp{cls.user1.id}", creator=cls.user1)
    
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
        self.assertEqual(self.user1.get_temp_checklist(), self.check)

class LoginRequestTest(TestCase):
    def setUp(self):
        self.credentials = {'username': "user1@test.com", 'password': "u0hN500N"}
        User.objects.create_user(self.credentials['username'], "Test User", self.credentials['password'])
    
    def test_login(self):
        response = self.client.post(reverse('user_app:login'), self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('cl_app:user_checklists'))

class RegisterRequestTest(TestCase):
    def setUp(self):
        self.information = {
            'name': "Test User",
            'email': "user1@test.com",
            'password1': "u0hN500N",
            'password2': "u0hN500N",
        }

    def test_register_request(self):
        response = self.client.post(reverse('user_app:register'), self.information, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('cl_app:user_checklists'))
