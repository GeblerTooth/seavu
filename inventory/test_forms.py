from django.test import TestCase
from django.contrib.auth.models import User

from .models import Software
from .forms import UserRegisterForm, EmployeeRegisterForm, AuthenticationForm, ComputerForm, SoftwareForm

from secrets import token_urlsafe

class TestForms(TestCase):

    def setUp(self):
        self.test_username, self.test_password = ('test_user', token_urlsafe(16))
        self.test_user = User.objects.create_user(username=self.test_username, password=self.test_password)

    def test_user_register_form_succeeds(self):
        form = UserRegisterForm(data={'email': 'test@example.com', 'username': 'test_user_2', 'password1': 'test_user_password', 'password2': 'test_user_password'})
        self.assertTrue(form.is_valid())

    def test_employee_register_form_succeeds(self):
        form = EmployeeRegisterForm(data={'user': self.test_user, 'occupation': 'Other', 'department': 'Testing'})
        self.assertTrue(form.is_valid())

    def test_authentication_form_succeeds(self):
        form = AuthenticationForm(self.client.request(), data={'username': self.test_username, 'password': self.test_password})
        self.assertTrue(form.is_valid())
        self.assertTrue(self.client.login(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password')))

    def test_software_form_succeeds(self):
        form = SoftwareForm(data={'name': 'test_software', 'company_requisite': False, 'has_licence': True})
        self.assertTrue(form.is_valid())

    def test_computer_form_succeeds(self):
        test_software = Software.objects.create(name='test_software', company_requisite=False, has_licence=True)
        form = ComputerForm(data={'name': 'test_computer', 'status': 'Active', 'make': 'Tester', 'model': '1000', 'category': 'PC', 'software': [test_software.pk]})
        self.assertTrue(form.is_valid())