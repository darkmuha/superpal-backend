from django.urls import path

from .views import training_list, training_detail

urlpatterns = [
    path('', training_list, name="training_list"),  # Get all trainings, create training
    path('<str:training_id>/', training_detail, name="training_detail"),  # Get, Update, and Delete a training
]
