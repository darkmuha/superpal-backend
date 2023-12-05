from django.urls import path

from .views import training_list, training_detail

urlpatterns = [
    path('', training_list, name="training-list"),  # Get all trainings, create training
    path('<uuid:training_id>/', training_detail, name="training-detail"),  # Get, Update, and Delete a training
]
