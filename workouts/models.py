import uuid

from django.db import models

from utils.enums import Difficulty, Intensity
from trainings.models import Training


# Create your models here.
class Workout(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40, unique=True)
    difficulty = models.TextField(choices=Difficulty.choices)
    intensity = models.TextField(choices=Intensity.choices)

    def __str__(self):
        return self.name


class WorkoutTraining(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workout_id = models.ForeignKey(Workout, on_delete=models.CASCADE)
    training_id = models.ForeignKey(Training, on_delete=models.CASCADE)

    def __str__(self):
        return f"WorkoutTraining {self.id}: Workout={self.workout_id.name}, Training={self.training_id.video}"
