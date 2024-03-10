from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()
from .models import Employee, Computer, Software
from .forms import UserRegisterForm, EmployeeRegisterForm, ComputerForm, SoftwareForm

class TestForms(TestCase):

    def test_user_register_form(self):
        form = UserRegisterForm(data={'email': 'test_user@example.com', 'username': 'test_user', 'password1': 'test_user_password', 'password2': 'test_user_password'})
        self.assertTrue(form.is_valid())

    def test_employee_register_form(self):
        test_user = User.objects.create(username='test_user', password='test_user_password')
        form = EmployeeRegisterForm(data={'user': test_user, 'occupation': 'Other', 'department': 'Testing'})
        self.assertTrue(form.is_valid())

    def test_software_form(self):
        form = SoftwareForm(data={'name': 'test_software', 'company_requisite': False, 'has_licence': True})
        self.assertTrue(form.is_valid())

    def test_computer_form(self):
        test_software = Software.objects.create(name='test_software', company_requisite=False, has_licence=True)
        form = ComputerForm(data={'name': 'test_computer', 'status': 'Active', 'make': 'Tester', 'model': '1000', 'category': 'PC', 'software': [test_software.pk]})
        self.assertTrue(form.is_valid())