from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Customer
from .serializers import CustomerSerializer, UserSerializer


# Create your views here.
@api_view(['GET', 'POST'])
def customer_list(request):
    """
    List all customers(Temporary)
    """
    if request.method == 'GET':
        customers = Customer.objects.all()

        serializer = CustomerSerializer(instance=customers, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def customer_detail(request, customer_id):
    """
    get, update or delete an employee.
    """
    customer = get_object_or_404(Customer, pk=customer_id)

    if request.method == 'GET':
        serializer = CustomerSerializer(instance=customer)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        data = request.data

        if data.get('is_admin', 'false').lower() == 'true':
            return Response(data="Can't change customer to admin through this route",
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomerSerializer(instance=customer, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        customer.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
