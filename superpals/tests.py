from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import User
from .models import SuperPals, SuperPalWorkoutRequest
from utils.enums import SuperPalWorkoutRequestStatus


class SuperPalsTests(APITestCase):
    def setUp(self):
        self.user1_data = {
            'email': 'john.doe1@example.com',
            'username': 'john_doe1',
            'password': 'password123',
        }
        self.user1 = User.objects.create_user(**self.user1_data)

        self.user2_data = {
            'email': 'john.doe2@example.com',
            'username': 'john_doe2',
            'password': 'password123',
        }
        self.user2 = User.objects.create_user(**self.user2_data)
        self.superpal = SuperPals.objects.create(user=self.user1, pal=self.user2)

    def test_superpal_list_all(self):
        url = reverse('superpal-list-all')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_superpal_list_user(self):
        url = reverse('superpal-list-user', args=[str(self.user1.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_superpal_detail(self):
        url = reverse('superpal-detail', args=[str(self.superpal.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['user']), str(self.superpal.user.id))
        self.assertEqual(str(response.data['pal']), str(self.superpal.pal.id))

    def test_superpal_delete(self):
        url = reverse('superpal-detail', args=[str(self.superpal.id)])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SuperPals.objects.count(), 0)


class SuperPalWorkoutRequestTests(APITestCase):
    def setUp(self):
        self.sender_data = {
            'email': 'john.doe1@example.com',
            'username': 'john_doe1',
            'password': 'password123',
        }
        self.sender = User.objects.create_user(**self.sender_data)

        self.recipient_data = {
            'email': 'john.doe2@example.com',
            'username': 'john_doe2',
            'password': 'password123',
        }
        self.recipient = User.objects.create_user(**self.recipient_data)
        self.extra_recipient_data = {
            'email': 'john.doe3@example.com',
            'username': 'john_doe3',
            'password': 'password123',
        }
        self.extra_recipient = User.objects.create_user(**self.extra_recipient_data)
        self.workout_request = SuperPalWorkoutRequest.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            workout_time='2024-01-01T12:00:00Z',
        )

    def test_workout_request_list(self):
        url = reverse('workout-request-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_workout_request_detail(self):
        url = reverse('workout-request-detail', args=[str(self.workout_request.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['sender']['id']), str(self.sender.id))
        self.assertEqual(str(response.data['recipient']['id']), str(self.recipient.id))

    def test_workout_request_create(self):
        url = reverse('workout-request-list')
        data = {
            'sender_id': str(self.sender.id),
            'recipient_id': str(self.extra_recipient.id),
            'workout_time': '2024-01-01T14:00:00Z',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SuperPalWorkoutRequest.objects.count(), 2)

    def test_workout_request_update_status(self):
        url = reverse('workout-request-detail', args=[str(self.workout_request.id)])
        data = {'status': SuperPalWorkoutRequestStatus.ACCEPTED}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.workout_request.refresh_from_db()
        self.assertEqual(self.workout_request.status, str(SuperPalWorkoutRequestStatus.ACCEPTED))

    def test_workout_request_update_status_to_completed(self):
        url = reverse('workout-request-detail', args=[str(self.workout_request.id)])
        data = {'status': SuperPalWorkoutRequestStatus.COMPLETED}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.workout_request.refresh_from_db()
        self.assertEqual(self.workout_request.status, str(SuperPalWorkoutRequestStatus.COMPLETED))

        sender_pal_instance = SuperPals.objects.filter(user=self.sender, pal=self.recipient).first()

        self.assertIsNotNone(sender_pal_instance)
