import logging

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.custom_exceptions import InvalidInputFormatException
from utils.logger_decorator import log_handler_decorator
from .models import Customer
from .serializers import CustomerSerializer, UserSerializer

logger = logging.getLogger(__name__)


# Create your views here.
@api_view(['GET'])
@log_handler_decorator(logger)
def customer_list(request):
    """
    List all customers(Temporary)
    """
    if request.method == 'GET':
        customers = Customer.objects.all()

        serializer = CustomerSerializer(instance=customers, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@log_handler_decorator(logger)
def customer_detail(request, customer_id):
    """
    get, update or delete an employee.
    """
    customer = get_object_or_404(Customer, pk=customer_id)
    user = customer.user

    if request.method == 'GET':
        serializer = CustomerSerializer(instance=customer)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        data = request.data

        if data.get('is_admin', False):
            return Response(data="Can't change customer to admin through this route",
                            status=status.HTTP_400_BAD_REQUEST)

        customer_serializer = CustomerSerializer(instance=customer, data=data, partial=True)

        if customer_serializer.is_valid():
            if data.get('user'):
                old_password = data['user'].pop('old_password', None)
                new_password = data['user'].pop('new_password', None)
                retype_new_password = data['user'].pop('retype_new_password', None)

                if old_password and new_password and retype_new_password:
                    if not check_password(old_password, user.password):
                        return Response(data={'old_password': ['Incorrect old password']},
                                        status=status.HTTP_400_BAD_REQUEST)
                    if new_password != retype_new_password:
                        return Response(data={'new_password': ['New password and retype password do not match']},
                                        status=status.HTTP_400_BAD_REQUEST)
                    user.set_password(new_password)

                user_serializer = UserSerializer(instance=user, data=data.get('user'), partial=True)
                if not user_serializer.is_valid():
                    raise InvalidInputFormatException(user_serializer.errors.items())
                user_serializer.save()

            # Update customer and associated user with the modified serializer
            customer_serializer.update(customer, data)

            return Response(data=customer_serializer.data, status=status.HTTP_200_OK)

        raise InvalidInputFormatException(customer_serializer.errors.items())
    elif request.method == 'DELETE':
        customer.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
