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
    trainings = models.ManyToManyField(Training)
    rest_between_trainings = models.PositiveIntegerField()

    def __str__(self):
        return self.name
