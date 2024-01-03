from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from utils.custom_exceptions import InvalidInputFormatException
from .serializers import TrainingSerializer
from .models import Training


@api_view(['GET', 'POST'])
def training_list(request):
    """
    List of all workouts AND Create a new training
    """
    if request.method == 'GET':
        trainings = Training.objects.all()

        serializer = TrainingSerializer(instance=trainings, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = TrainingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        raise InvalidInputFormatException(serializer.errors.items())


@api_view(['GET', 'PUT', 'DELETE'])
def training_detail(request, training_id):
    """
    GET, UPDATE or DELETE a training.
    """

    training = get_object_or_404(Training, pk=training_id)
    if request.method == 'GET':
        serializer = TrainingSerializer(instance=training)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = TrainingSerializer(instance=training, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        raise InvalidInputFormatException(serializer.errors.items())

    elif request.method == 'DELETE':
        training.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
