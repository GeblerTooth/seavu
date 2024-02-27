from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()
from .models import Software

from .test_auth import create_test_user

class TestComputer(TestCase):

    def setUp(self):
        self.test_user_name, self.test_user_password = create_test_user('test_user_name')
        self.client.login(username=self.test_user_name, password=self.test_user_password) # Login for following tests that require authentication.

        Software.objects.create(name='test-software-1', company_requisite=True, has_licence=True)

    def test_software(self):
        response = self.client.get('/software')
        self.assertEqual(response.status_code, 200)

    def test_add_software(self):
        response = self.client.post('/software/add', data = {
            'name': 'test-software-2',
            'company_requisite': False,
            'has_licence': False
        })
        self.assertRedirects(response, '/software') # Test for redirect after sucessful software addition.
        self.assertEqual(Software.objects.all().count(), 2)
        self.assertNotEqual(User.objects.filter(id=1).first(), None)

    def test_inspect_software(self):
        response = self.client.get('/software/1')
        self.assertEqual(response.status_code, 200)