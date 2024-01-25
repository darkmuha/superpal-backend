from django.urls import path

from .views import customer_list, customer_detail, progress_detail, progress_list

urlpatterns = [
    path('', customer_list, name='customer-list'),  # get all customers(temporary)
    path('<uuid:customer_id>/', customer_detail, name='customer-detail'),  # get, update, delete a customer
    path('progress/<uuid:customer_id>/', progress_detail, name='progress-detail'),
    path('progress/', progress_list, name='progress-list'),
]
