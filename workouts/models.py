import uuid

from django.db import models

from utils.enums import Difficulty, Intensity


# Create your models here.
class Workout(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40, unique=True)
    difficulty = models.CharField(choices=Difficulty.choices)
    intensity = models.CharField(choices=Intensity.choices)

    def __str__(self):
        return self.name


class Training(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video = models.CharField(max_length=255)
    repetitions = models.PositiveIntegerField()
    sets = models.PositiveIntegerField()

    def __str__(self):
        return f"Training {self.id}: Reps={self.repetitions}, Sets={self.sets}"


class WorkoutTraining(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workout_id = models.ForeignKey(Workout, on_delete=models.CASCADE)
    training_id = models.ForeignKey(Training, on_delete=models.CASCADE)

    def __str__(self):
        return f"WorkoutTraining {self.id}: Workout={self.workout_id.name}, Training={self.training_id.video}"
