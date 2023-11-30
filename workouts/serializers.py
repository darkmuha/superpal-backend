from rest_framework import serializers

from trainings.serializers import TrainingSerializer
from .models import Workout


class WorkoutSerializer(serializers.ModelSerializer):
    trainings = TrainingSerializer(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = '__all__'
