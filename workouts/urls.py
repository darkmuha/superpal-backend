from django.urls import path

from .views import workout_list, workout_detail

urlpatterns = [
    path('', workout_list, name="workout-list"),  # Get all workouts, create workout
    path('<str:workout_id>/', workout_detail, name="workout-detail"),  # Get, Update, and Delete a workout
]
