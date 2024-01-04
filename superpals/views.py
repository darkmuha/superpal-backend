import logging

from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import SuperPals, SuperPalWorkoutRequest
from .serializers import SuperPalsSerializer, SuperPalWorkoutRequestSerializer
from authentication.models import User
from utils.logger_decorator import log_handler_decorator

logger = logging.getLogger(__name__)


# Create your views here.
@api_view(['GET'])
@log_handler_decorator(logger)
def superpal_list_all(request):
    if request.method == 'GET':
        superpals = SuperPals.objects.all()

        serializer = SuperPalsSerializer(instance=superpals, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@log_handler_decorator(logger)
def superpal_list_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'GET':
        superpals = SuperPals.objects.filter(Q(user=user) | Q(pal=user))

        serializer = SuperPalsSerializer(instance=superpals, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE'])
@log_handler_decorator(logger)
def superpal_detail(request, superpal_id):
    superpal = get_object_or_404(SuperPals, pk=superpal_id)

    if request.method == 'GET':
        serializer = SuperPalsSerializer(instance=superpal)

        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        superpal.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@log_handler_decorator(logger)
def workout_request_list(request):
    if request.method == 'GET':
        workout_requests = SuperPalWorkoutRequest.objects.all()

        serializer = SuperPalWorkoutRequestSerializer(instance=workout_requests, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        sender_id = request.data.get('sender_id', None)
        recipient_id = request.data.get('recipient_id', None)

        if sender_id is None or recipient_id is None:
            return Response(data={'error': 'Both sender_id and recipient_id are required in the request data.'},
                            status=status.HTTP_400_BAD_REQUEST)

        sender = get_object_or_404(User, pk=sender_id)
        recipient = get_object_or_404(User, pk=recipient_id)

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
