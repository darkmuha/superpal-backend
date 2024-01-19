from django.urls import path

from .views import (
    superpal_list_customer,
    superpal_list_all,
    superpal_detail,
    workout_request_list_all,
    workout_request_detail,
    workout_request_list_customer,
)

urlpatterns = [
    path('', superpal_list_all, name='superpal-list-all'),  # Get superpals
    path('customer/<uuid:customer_id>/', superpal_list_customer, name='superpal-list-customer'),
    # Get superpals for a customer
    path('detail/<uuid:superpal_id>/', superpal_detail, name='superpal-detail'),  # Get superpal, and Delete superpal
    path('workout_request/', workout_request_list_all, name='workout-request-list-all'),
    # Get workout_requests, Create workout_request
    path('workout_request/customer/<uuid:customer_id>/', workout_request_list_customer,
         name='workout-request-list-customer'),
    path('workout_request/<uuid:workout_request_id>/', workout_request_detail, name='workout-request-detail'),
    # Get workout_request, delete workout_request and update workout request status.
]
