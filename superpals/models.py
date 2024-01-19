import uuid

from django.db import models

from authentication.models import User
from customers.models import Customer
from utils.enums import SuperPalWorkoutRequestStatus


class SuperPals(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='superpals_user')
    pal = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='superpals_pal_user')

    def __str__(self):
        return f"{self.user}'s Super Pal: {self.pal}"


class SuperPalWorkoutRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sender_requests')
    recipient = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='recipient_requests')
    workout_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=SuperPalWorkoutRequestStatus.choices,
                              default=SuperPalWorkoutRequestStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Workout Request from {self.sender_id} to {self.recipient_id} at {self.workout_time}"

    def update_status(self, new_status):
        current_status = self.status

        # Define the allowed status transitions
        allowed_transitions = {
            'Pending': ['Accepted', 'Canceled'],
            'Accepted': ['Completed', 'Canceled'],
        }

        # Check if the new status is allowed based on the current status
        if current_status in allowed_transitions and new_status in allowed_transitions[current_status]:
            self.status = new_status
            self.save()
            return True
        else:
            return False
