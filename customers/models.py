import uuid

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from utils.enums import SexType, Intensity, Difficulty, Rank
from workouts.models import Workout, Training
from authentication.models import User


# Create your models here.
class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    sex = models.TextField(choices=SexType.choices)
    profile_picture = models.CharField(max_length=255, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    age = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0),
        ]
    )
    workout_selected = models.ForeignKey(Workout, on_delete=models.SET_NULL, null=True)
    workout_streak = models.IntegerField(default=0)
    workout_intensity = models.TextField(choices=Intensity.choices)
    workout_difficulty = models.TextField(choices=Difficulty.choices)
    rank = models.IntegerField(choices=Rank.choices, default=Rank.WARRIOR)
    current_gym = models.CharField(max_length=40)
    current_location = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    progress_image = models.CharField(max_length=255)
    taken_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Progress for {self.user} at {self.taken_at}"


class CustomerTrainingStats(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    current_weight = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.customer}'s training stats for {self.training.name}"
