from rest_framework import serializers
from django.shortcuts import get_object_or_404

from trainings.serializers import TrainingSerializer
from .models import Workout
from trainings.models import Training


class WorkoutSerializer(serializers.ModelSerializer):
    trainings = TrainingSerializer(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = '__all__'
