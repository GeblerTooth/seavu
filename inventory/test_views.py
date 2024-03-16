from django.test import TestCase
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.urls import reverse

from secrets import token_urlsafe

from .models import Employee, Computer, Software

class TestViews(TestCase):

    def setUp(self):
        self.test_username, self.test_password = ('test_user', token_urlsafe(16))
        self.test_user = User.objects.create_user(username=self.test_username, password=self.test_password)
        self.client.force_login(self.test_user)

        self.computer1 = Computer.objects.create(name='Computer 1', status='Active', make='Tester', model='1000', category='PC')
        self.computer2 = Computer.objects.create(name='Computer 2', status='Active', make='Tester', model='1000', category='PC')

        self.software1 = Software.objects.create(name='Software 1', company_requisite=True, has_licence=False)
        self.software2 = Software.objects.create(name='Software 2', company_requisite=False, has_licence=True)

    def test_inventory_view_status_code(self):
        response = self.client.get(reverse('inventory'))
        self.assertEqual(response.status_code, 200)

    def test_inventory_view_template(self):
        response = self.client.get(reverse('inventory'))
        self.assertTemplateUsed(response, 'inventory/inventory.html')

    def test_inventory_view_context(self):
        response = self.client.get(reverse('inventory'))
        self.assertIn('computer_list', response.context)
        computer_list = response.context['computer_list']
        self.assertEqual(len(computer_list), 2)
        self.assertIn(self.computer1, computer_list)
        self.assertIn(self.computer2, computer_list)

    def test_add_computer_view_status_code(self):
        response = self.client.get(reverse('add-computer'))
        self.assertEqual(response.status_code, 200)

    def test_add_computer_view_template(self):
        response = self.client.get(reverse('add-computer'))
        self.assertTemplateUsed(response, 'inventory/add_computer.html')

    def test_add_computer_view_context(self):
        response = self.client.get(reverse('add-computer'))
        self.assertIn('form', response.context)

    def test_add_computer_view_function(self):
        response = self.client.post(reverse('add-computer'), {'name': 'Computer 3', 'category': 'PC','status': 'Active','make': 'Tester','model': '1000', 'software': []})
        self.assertEqual(Computer.objects.all().count(), 3)
        self.assertRedirects(response, reverse('inventory'))

    def test_update_computer_view_status_code(self):
        response = self.client.get(reverse('update-computer', args=[self.computer1.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_update_computer_view_template(self):
        response = self.client.get(reverse('update-computer', args=[self.computer1.pk]))
        self.assertTemplateUsed(response, 'inventory/update_computer.html')

    def test_update_computer_view_context(self):
        response = self.client.get(reverse('update-computer', args=[self.computer1.pk]))
        self.assertIn('form', response.context)

    def test_update_computer_view_function(self):
        response = self.client.post(reverse('update-computer', kwargs={'computer_id': 1}), {'name': 'Computer 1.5', 'status': 'Inactive', 'make': 'Tester', 'model': '1500', 'category': 'PC'})
        self.assertEqual(Computer.objects.get(id=1).name, 'Computer 1.5')
        self.assertEqual(Computer.objects.get(id=1).status, 'Inactive')
        self.assertEqual(Computer.objects.get(id=1).model, '1500')
        self.assertEqual(response.status_code, 200)

    def test_delete_computer_view_function_fails(self):
        response = self.client.post(reverse('delete-computer', kwargs={'computer_id': 1}))
        self.assertEqual(Computer.objects.all().count(), 2)
        self.assertEqual(response.status_code, 302)

    def test_software_view_status_code(self):
        response = self.client.get(reverse('software'))
        self.assertEqual(response.status_code, 200)

    def test_software_view_template(self):
        response = self.client.get(reverse('software'))
        self.assertTemplateUsed(response, 'inventory/software.html')
    
    def test_software_view_context(self):
        response = self.client.get(reverse('software'))
        self.assertIn('software_list', response.context)

    def test_add_software_view_status_code(self):
        response = self.client.get(reverse('add-software'))
        self.assertEqual(response.status_code, 200)

    def test_add_software_view_template(self):
        response = self.client.get(reverse('add-software'))
        self.assertTemplateUsed(response, 'inventory/add_software.html')

    def test_add_software_view_context(self):
        response = self.client.get(reverse('add-software'))
        self.assertIn('form', response.context)
    
    def test_add_software_view_function(self):
        response = self.client.post(reverse('add-software'), {'name': 'Software 3', 'company_requisite': False, 'has_licence': False})
        self.assertEqual(Software.objects.all().count(), 3)
        self.assertRedirects(response, reverse('software'))

    def test_update_computer_view_status_code(self):
        response = self.client.get(reverse('update-software', args=[self.software1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_update_software_view_template(self):
        response = self.client.get(reverse('update-software', args=[self.software1.pk]))
        self.assertTemplateUsed(response, 'inventory/update_software.html')

    def test_update_software_view_context(self):
        response = self.client.get(reverse('update-software', args=[self.software1.pk]))
        self.assertIn('form', response.context)

    def test_update_software_view_function(self):
        response = self.client.post(reverse('update-software', kwargs={'software_id': 1}), {'name': 'Software 1.5', 'company_requisite': False, 'has_licence': True})
        self.assertEqual(Software.objects.get(id=1).name, 'Software 1.5')
        self.assertEqual(Software.objects.get(id=1).company_requisite, False)
        self.assertEqual(Software.objects.get(id=1).has_licence, True)
        self.assertEqual(response.status_code, 200)

    def test_delete_software_view_function_fails(self):
        response = self.client.post(reverse('delete-software', kwargs={'software_id': 1}))
        self.assertEqual(Software.objects.all().count(), 2)
        self.assertEqual(response.status_code, 302)

class TestAuthViews(TestCase):

    def setUp(self):
        self.test_username, self.test_password = ('test_user', token_urlsafe(16))
        self.test_user = User.objects.create_user(username=self.test_username, password=self.test_password)

    def test_login_view_status_code(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_redirects_user(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('inventory'))

    def test_login_view_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_view_context(self):
        response = self.client.get(reverse('login'))
        self.assertIn('form', response.context)

    def test_login_view_function(self):
        response = self.client.post(reverse('login'), {'username': self.test_username, 'password': self.test_password})
        self.assertRedirects(response, reverse('inventory'))
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_register_view_status_code(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
    
    def test_register_view_template(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response,'registration/register.html')
    
    def test_register_view_context(self):
        response = self.client.get(reverse('register'))
        self.assertIn('user_form', response.context)
        self.assertIn('employee_form', response.context)

    def test_register_view_function(self):
        username, password = ('johndoe', token_urlsafe(16))
        response = self.client.post(reverse('register'), {
            'username': username,
            'password1': password,
            'password2': password,
            'email': 'johndoe@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'occupation': 'Other',
            'department': 'Testing',
        })
        self.assertRedirects(response, reverse('inventory')) # Test automatic login successful.
        user = get_user(self.client)
        self.assertEqual(User.objects.get(id=user.id), user)
        try:
            Employee.objects.get(user=user)
        except:
            self.fail('Employee was not created during registration.')

    def test_logout(self):
        self.client.force_login(self.test_user)
        self.client.logout()
        self.assertFalse(get_user(self.client).is_authenticated)

class TestAdminViews(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_superuser(username='test_superuser', password=token_urlsafe(16))
        self.client.force_login(self.test_user)

        self.computer1 = Computer.objects.create(name='Computer 1', status='Active', make='Tester', model='1000', category='PC')
        self.computer2 = Computer.objects.create(name='Computer 2', status='Active', make='Tester', model='1000', category='PC')

        self.software1 = Software.objects.create(name='Software 1', company_requisite=True, has_licence=False)
        self.software2 = Software.objects.create(name='Software 2', company_requisite=False, has_licence=True)

    def test_delete_computer_view_function(self):
        response = self.client.post(reverse('delete-computer', kwargs={'computer_id': 1}))
        self.assertEqual(Computer.objects.all().count(), 1)
        self.assertRaises(Computer.DoesNotExist, Computer.objects.get, id=1)

    def test_delete_software_view_function(self):
        response = self.client.post(reverse('delete-software', kwargs={'software_id': 1}))
        self.assertEqual(Software.objects.all().count(), 1)
        self.assertRaises(Software.DoesNotExist, Software.objects.get, id=1)