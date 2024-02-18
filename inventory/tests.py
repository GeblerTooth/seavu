from django.test import TestCase
from django.contrib.auth import get_user_model, get_user

User = get_user_model()

from .models import Employee

from secrets import token_urlsafe

class Auth(TestCase):

    def setUp(self):
        self.test_user_name = 'test_user_name'
        self.test_user_password = token_urlsafe(16) # Random URL safe password.
        test_user = User.objects.create_user(username=self.test_user_name, password=self.test_user_password)
        test_user.save()

    def test_register(self):
        register_test_password = token_urlsafe(16) # Random URL safe password.
        response = self.client.post('/register', data = {
            'username': 'register_test_user',
            'email': 'register-test@register-test.com',
            'first_name': 'register_test_first_name',
            'last_name': 'register_test_last_name',
            'password1': register_test_password,
            'password2': register_test_password,
            'occupation': 1,
            'department': 'testing'
        })
        self.assertEqual(response.status_code, 200)
        # Test both User and Employee created as OneToOne relationship.
        self.assertEqual(User.objects.all().count(), 2)
        self.assertNotEqual(User.objects.filter(id=2).first(), None)
        self.assertNotEqual(User.objects.filter(username='register_test_user').first(), None)
        self.assertEqual(Employee.objects.all().count(), 1)
        self.assertNotEqual(Employee.objects.filter(id=1).first(), None)
        self.assertNotEqual(Employee.objects.filter(user=User.objects.get(username='register_test_user')).first(), None) # Test Employee exists with link to User created.

    def test_login(self):
        self.assertTrue(self.client.login(username=self.test_user_name, password=self.test_user_password))
        response = self.client.get('/')
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_logout(self):
        self.client.login(username=self.test_user_name, password=self.test_user_password)
        self.client.logout()
        response = self.client.get('/login')
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_home_redirect_for_login_required(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login/?next=/')
        self.client.login(username=self.test_user_name, password=self.test_user_password)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)