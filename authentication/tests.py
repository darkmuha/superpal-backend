from django.contrib.auth import authenticate
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from customers.models import Customer
from authentication.models import User
from utils.enums import Intensity, Difficulty


class AuthenticationViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'john.doe@example.com',
            'username': 'john_doe',
            'password': 'password123',
        }
        self.user = User.objects.create_user(**self.user_data)  # Used default .create_user since it hashes the password
        self.customer_data = {
            'user': self.user,
            'first_name': 'John',
            'last_name': 'Doe',
            'sex': 'Male',
            'weight': 75.5,
            'height': 175.0,
            'age': 30,
            'workout_intensity': 'HIGH',
            'workout_difficulty': 'PRO',
            'current_gym': 'Gym Name',
            'current_location': 'City',
        }
        self.customer = Customer.objects.create(**self.customer_data)

    def test_login_view(self):
        url = reverse('login')
        data = {'email': self.user_data['email'], 'password': self.user_data['password']}
        response = self.client.post(url, data)

        user = authenticate(username=self.user_data['email'], password=self.user_data['password'])
        self.assertIsNotNone(user,
                             msg=f"User with email {self.user_data['email']} not found in authentication backend.")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_login_view(self):
        url = reverse('login')
        data = {'email': self.user_data['email'], 'password': 'wrong_password'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, "Invalid email or password")

    def test_signup_view(self):
        url = reverse('register')
        data = {
            'user': {
                'email': 'new_user@example.com',
                'username': 'new_user',
                'password': 'new_password',
            },
            'first_name': 'New',
            'last_name': 'User',
            'sex': 'Male',
            'weight': 70.0,
            'height': 180.0,
            'age': 25,
            'workout_intensity': Intensity.LOW,
            'workout_difficulty': Difficulty.BEGINNER,
            'current_gym': 'New Gym',
            'current_location': 'New City',
        }

        content = JSONRenderer().render(data)
        response = self.client.post(url, content, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)  # One customer from setup and one from here

    def test_invalid_signup_view(self):
        url = reverse('register')
        data = {'email': 'invalid_email', 'username': 'new_user', 'password': 'new_password'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_view(self):
        url = reverse('logout')
        refresh_token = RefreshToken.for_user(self.user)
        data = {'refresh_token': str(refresh_token)}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        blacklisted_token = BlacklistedToken.objects.filter(token=refresh_token)
        self.assertTrue(blacklisted_token.exists(),
                        msg="Refresh token not blacklisted")

    def test_create_admin_view(self):
        url = reverse('create-admin')
        data = {
            'email': 'admin@example.com',
            'username': 'admin_user',
            'password': 'admin_password',
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=data['email'], is_admin=True).exists())
