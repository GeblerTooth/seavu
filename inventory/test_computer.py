from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()
from .models import Computer

from .test_auth import create_test_user

class TestComputer(TestCase):

    def setUp(self):
        self.test_user_name, self.test_user_password = create_test_user('test_user_name')
        self.client.login(username=self.test_user_name, password=self.test_user_password) # Login for following tests that require authentication.

        Computer.objects.create(name='test-computer-1', status='Active', make='Tester', model='1000', category='PC')

    def test_inventory(self):
        response = self.client.get('/inventory')
        self.assertEqual(response.status_code, 200)

    def test_add_computer(self):
        response = self.client.post('/computer/add', data = {
            'name': 'test-computer-2',
            'status': 'Active',
            'make': 'Tester',
            'model': '2000',
            'category': 'Laptop' 
        })
        self.assertRedirects(response, '/inventory') # Test for redirect after sucessful computer addition.
        self.assertEqual(Computer.objects.all().count(), 2)
        self.assertNotEqual(User.objects.filter(id=1).first(), None)

    def test_inspect_computer(self):
        response = self.client.get('/computer/1')
        self.assertEqual(response.status_code, 200)