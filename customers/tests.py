from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from utils.enums import Intensity, Difficulty
from .models import Customer
from authentication.models import User


class CustomerViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='john.doe@example.com', username='john_doe')
        self.user.set_password('somePassword123$')
        self.user.save()
        
        self.customer_data = {
            'user': self.user,
            'first_name': 'John',
            'last_name': 'Doe',
            'sex': 'Male',
            'weight': 75.5,
            'height': 175.0,
            'age': 30,
            'workout_intensity': Intensity.HIGH,
            'workout_difficulty': Difficulty.PRO,
            'current_gym': 'Gym Name',
            'current_location': 'City',
        }
        self.customer = Customer.objects.create(**self.customer_data)

    def test_customer_list(self):
        url = reverse('customer-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_customer_detail_get(self):
        url = reverse('customer-detail', args=[str(self.customer.id)])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.customer_data['first_name'])
        self.assertEqual(response.data['last_name'], self.customer_data['last_name'])
        self.assertEqual(response.data['user']['email'], self.customer_data['user'].email)

    def test_customer_detail_put(self):
        url = reverse('customer-detail', args=[str(self.customer.id)])
        updated_data = {
            'first_name': 'Updated John',
            'last_name': 'Updated Doe',
            'weight': 80.0,
            'height': 180.0,
            'age': 32,
            'workout_intensity': Intensity.LOW,
            'workout_difficulty': Difficulty.BEGINNER,
            'current_gym': 'Updated Gym Name',
            'current_location': 'Updated City',
            'user': {
                'old_password': 'somePassword123$',
                'new_password': 'somePassword123$$$$',
                'retype_new_password': 'somePassword123$$$$',
                'username': 'HelloThere'
            }
        }
        response = self.client.put(url, data=updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.first_name, updated_data['first_name'])
        self.assertEqual(self.customer.last_name, updated_data['last_name'])
        self.assertEqual(self.customer.weight, updated_data['weight'])
        self.assertEqual(self.customer.height, updated_data['height'])
        self.assertEqual(self.customer.age, updated_data['age'])
        self.assertEqual(self.customer.workout_intensity, updated_data['workout_intensity'])
        self.assertEqual(self.customer.workout_difficulty, updated_data['workout_difficulty'])
        self.assertEqual(self.customer.current_gym, updated_data['current_gym'])
        self.assertEqual(self.customer.current_location, updated_data['current_location'])
        self.assertEqual(self.customer.user.username, updated_data['user'].get('username'))

    def test_customer_detail_delete(self):
        url = reverse('customer-detail', args=[str(self.customer.id)])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 0)
