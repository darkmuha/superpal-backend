from django.urls import path

from .views import customer_list, customer_detail, create_admin

urlpatterns = [
    path('', customer_list, name='customer-list'),  # get all customers(temporary), create new customer
    path('<uuid:customer_id>/', customer_detail, name='customer-detail'),  # get, update, delete a customer
    path('admin/', create_admin, name='create-admin')  # create admin user
]
