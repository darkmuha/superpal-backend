from django.urls import path

from .views import (
    superpal_list_user,
    superpal_list_all,
    superpal_detail,
    workout_request_list,
    workout_request_detail
)

urlpatterns = [
    path('', superpal_list_all, name='superpal-list-all'),  # Get superpals
    path('user/<uuid:user_id>/', superpal_list_user, name='superpal-list-user'),  # Get superpals for a user
    path('detail/<uuid:superpal_id>/', superpal_detail, name='superpal-detail'),  # Get superpal, and Delete superpal
    path('workout_request/', workout_request_list, name='workout-request-list'),
    # Get workout_requests, Create workout_request
    path('workout_request/<uuid:workout_request_id>/', workout_request_detail, name='workout-request-detail'),
    # Get workout_request, delete workout_request and update workout request status.
]
