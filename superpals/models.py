import uuid

from django.db import models

from users.models import User


class SuperPals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='superpals_user')
    favorite_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='superpals_favorite_user')

    def __str__(self):
        return f"{self.user}'s Super Pal: {self.favorite_user}"


class SuperPalWorkoutRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_requests')
    recipient_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient_requests')
    workout_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Workout Request from {self.sender_id} to {self.recipient_id} at {self.workout_time}"
