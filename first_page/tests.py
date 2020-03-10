from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your tests here.

class FrontendTestCase(TestCase):
    def test_frontend_page(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)


class UserTestCase(TestCase):
    def test_singup_user(self):
        user_name     = 'test_username'
        user_password = 'test_password'
        client = Client()

        url = reverse('first_page:register_user')
        response = client.post(url, {
            'username' : user_name,
            'password' : user_password,
            'email' : 'test@example.com',
            'first_name': 'John',
            'last_name': 'Dohn',
            })

        self.assertEqual(response.status_code, 200)

        result = client.login(username=user_name, password=user_password)

        if not result:
            raise Exception('User does not exists. Signup failed or something goes wrong')

    def test_login_user(self):
        user_name     = 'test_username'
        user_password = 'test_password'
        client = Client()

        url = reverse('first_page:authenticate_user')
        response = client.post(url, {
            'username' : user_name,
            'password' : user_password,
            })

        self.assertEqual(response.status_code, 200)
