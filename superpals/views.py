import logging

from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication

from customers.models import Customer
from .models import SuperPals, SuperPalWorkoutRequest
from .serializers import SuperPalsSerializer, SuperPalWorkoutRequestSerializer, UserSuperPalsSerializer
from utils.logger_decorator import log_handler_decorator

logger = logging.getLogger(__name__)


# Create your views here.
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@log_handler_decorator(logger)
def superpal_list_all(request):
    if request.method == 'GET':
        superpals = SuperPals.objects.all()

        serializer = SuperPalsSerializer(instance=superpals, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@log_handler_decorator(logger)
def superpal_list_customer(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)

    if request.method == 'GET':
        superpals = SuperPals.objects.filter(Q(user=customer) | Q(pal=customer))

        serializer = UserSuperPalsSerializer(instance=superpals, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@log_handler_decorator(logger)
def superpal_detail(request, superpal_id):
    superpal = get_object_or_404(SuperPals, pk=superpal_id)

    if request.method == 'GET':
        serializer = SuperPalsSerializer(instance=superpal)

        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        superpal.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@log_handler_decorator(logger)
def workout_request_list_customer(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)

    if request.method == 'GET':
        workout_status = request.query_params.get('status', None)

        workout_requests = SuperPalWorkoutRequest.objects.filter(Q(sender=customer) | Q(recipient=customer))

        if workout_status:
            workout_requests = workout_requests.filter(status=workout_status)

        serializer = SuperPalWorkoutRequestSerializer(instance=workout_requests, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@log_handler_decorator(logger)
def workout_request_list_all(request):
    if request.method == 'GET':
        workout_status = request.query_params.get('status', None)

        workout_requests = SuperPalWorkoutRequest.objects.all()

        if workout_status:
            workout_requests = workout_requests.filter(status=workout_status)

        serializer = SuperPalWorkoutRequestSerializer(instance=workout_requests, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        sender_id = request.data.get('sender_id', None)
        recipient_id = request.data.get('recipient_id', None)

        if sender_id is None or recipient_id is None:
            return Response(data={'error': 'Both sender_id and recipient_id are required in the request data.'},
                            status=status.HTTP_400_BAD_REQUEST)
        sender = get_object_or_404(Customer, pk=sender_id)
        recipient = get_object_or_404(Customer, pk=recipient_id)

        request_data = {
            'sender': sender.id,
            'recipient': recipient.id,
            'workout_time': request.data.get('workout_time', None),
        }

        serializer = SuperPalWorkoutRequestSerializer(data=request_data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@log_handler_decorator(logger)
def workout_request_detail(request, workout_request_id):
    workout_request = get_object_or_404(SuperPalWorkoutRequest, pk=workout_request_id)
    if request.method == 'GET':
        serializer = SuperPalWorkoutRequestSerializer(instance=workout_request)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        workout_request_status = request.data.get('status', None)

        if workout_request_status is None:
            return Response(data={'error': 'Status is required in the request data.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if workout_request_status == 'Completed':
            superpals_request_data = {
                "user": workout_request.sender.id,
                "pal": workout_request.recipient.id,
            }
            superpals_serializer = SuperPalsSerializer(data=superpals_request_data)

            if not superpals_serializer.is_valid():
                return Response(data=superpals_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            superpals_serializer.save()

        update_data = {'status': workout_request_status}

        serializer = SuperPalWorkoutRequestSerializer(instance=workout_request, data=update_data,
                                                      partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        workout_request.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
