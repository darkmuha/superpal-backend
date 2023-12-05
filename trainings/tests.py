from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Training


class TrainingViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.training_data = {
            'name': 'Test Training',
            'video': 'https://example.com/test.mp4',
            'repetitions': 10,
            'sets': 3,
            'rest_between_sets': 60,
        }
        self.training = Training.objects.create(**self.training_data)

    def test_training_list(self):
        url = reverse('training-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_training(self):
        url = reverse('training-list')
        data = self.training_data
        data['name'] = 'Test Training 1'
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Training.objects.count(), 2)

    def test_training_detail(self):
        url = reverse('training-detail', args=[str(self.training.id)])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.training.id))

    def test_update_training(self):
        url = reverse('training-detail', args=[str(self.training.id)])
        updated_data = {
            'name': 'Updated Training',
            'video': 'https://example.com/updated.mp4',
            'repetitions': 15,
            'sets': 4,
            'rest_between_sets': 45,
        }
        response = self.client.put(url, data=updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.training.refresh_from_db()
        self.assertEqual(self.training.name, updated_data['name'])
        self.assertEqual(self.training.video, updated_data['video'])
        self.assertEqual(self.training.repetitions, updated_data['repetitions'])
        self.assertEqual(self.training.sets, updated_data['sets'])
        self.assertEqual(self.training.rest_between_sets, updated_data['rest_between_sets'])

    def test_delete_training(self):
        url = reverse('training-detail', args=[str(self.training.id)])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Training.objects.count(), 0)
