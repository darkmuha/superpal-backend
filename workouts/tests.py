from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from utils.enums import Difficulty, Intensity
from trainings.models import Training
from .models import Workout
from .serializers import WorkoutSerializer


class WorkoutViewsTestCase(TestCase):
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

        self.workout_data = {
            'name': 'Test Workout',
            'difficulty': Difficulty.BEGINNER,
            'intensity': Intensity.LOW,
            'rest_between_trainings': 120,
        }
        self.workout = Workout.objects.create(**self.workout_data)
        self.workout.trainings.set([self.training.id])
        self.workout_url = reverse('workout-detail', args=[str(self.workout.id)])

    def test_workout_list(self):
        url = reverse('workout-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_workout(self):
        url = reverse('workout-list')
        data = self.workout_data
        data['name'] = 'Test Workout 1'
        data['trainings'] = [str(self.training.id)]
        
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 2)

    def test_workout_detail(self):
        response = self.client.get(self.workout_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.workout.id))

    def test_update_workout(self):
        updated_data = {
            'name': 'Updated Workout',
            'difficulty': Difficulty.BEGINNER,
            'intensity': Intensity.MEDIUM,
            'rest_between_trainings': 90,
        }
        response = self.client.put(self.workout_url, data=updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.workout.refresh_from_db()
        self.assertEqual(self.workout.name, updated_data['name'])
        self.assertEqual(self.workout.difficulty, updated_data['difficulty'])
        self.assertEqual(self.workout.intensity, updated_data['intensity'])
        self.assertEqual(self.workout.rest_between_trainings, updated_data['rest_between_trainings'])

    def test_delete_workout(self):
        response = self.client.delete(self.workout_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Workout.objects.count(), 0)
