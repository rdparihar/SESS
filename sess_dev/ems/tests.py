from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import EmpProfile

class EmpProfileModelTests(TestCase):
    def test_str_returns_username(self):
        user = User.objects.create_user(username='john', password='pass')
        profile = EmpProfile.objects.create(
            username=user,
            emp_id=1,
            emp_dob='1990-01-01',
            emp_doj='2020-01-01',
            emp_con_primary='1234567890',
            emp_con_secondary='0987654321',
            emp_designation='Dev',
            emp_department='IT'
        )
        self.assertEqual(str(profile), 'john')

class EmployeeListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('employee'))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_uses_template(self):
        self.client.login(username='user', password='pass')
        response = self.client.get(reverse('employee'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ems/employee_list.html')
