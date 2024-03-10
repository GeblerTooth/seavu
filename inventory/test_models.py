from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()
from .models import Employee, Software, Computer

class TestModels(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test_user', password='test_user_password')
        self.test_employee = Employee.objects.create(user=self.test_user, occupation='Other', department='Testing')
        self.test_software = Software.objects.create(name='test_software', company_requisite=True, has_licence=True)
        self.test_computer = Computer.objects.create(name='test_computer', status='Active', make='Tester', model='1000')
        self.test_computer.software.add(self.test_software.pk)
    
    def test_user_model(self):
        self.assertEqual(self.test_user.username, 'test_user')

    def test_employee_model(self):
        self.assertEqual(self.test_employee.user, self.test_user)
        self.assertEqual(str(self.test_employee), self.test_user.username) # Test that the string representation of the employee is the same as the user's username.
    
    def test_software_model(self):
        self.assertEqual(self.test_software.name, 'test_software')
        self.assertEqual(str(self.test_software), self.test_software.name) # Test that the string representation of the software is the same as the software's name.

    def test_computer_model(self):
        self.assertEqual(self.test_computer.name, 'test_computer')
        self.assertEqual(str(self.test_computer), self.test_computer.name) # Test that the string representation of the computer is the same as the computer's name.
        self.assertEqual(list(self.test_computer.software.all()), [self.test_software]) # Test that the computer has a software associated with it.