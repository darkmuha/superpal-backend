import uuid

from django.db import models


# Create your models here.
class Training(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40, unique=True)
    video = models.CharField(max_length=255)
    repetitions = models.PositiveIntegerField()
    sets = models.PositiveIntegerField()
    rest_between_sets: models.PositiveIntegerField()

    def __str__(self):
        return f"Training {self.id}: Reps={self.repetitions}, Sets={self.sets}"
