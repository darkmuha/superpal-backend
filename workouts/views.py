import logging

from django.http import QueryDict
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from trainings.models import Training
from utils.custom_exceptions import InvalidInputFormatException
from utils.logger_decorator import log_handler_decorator
from .models import Workout
from .serializers import WorkoutSerializer

logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
@log_handler_decorator(logger)
def workout_list(request):
    """
    List of all workouts AND Create a new workout
    """
    if request.method == 'GET':
        workouts = Workout.objects.all()

        serializer = WorkoutSerializer(instance=workouts, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = QueryDict(mutable=True)
        data.update(request.data)
        trainings_ids = data.pop('trainings', None)
        if trainings_ids:
            if isinstance(trainings_ids[0], list):
                trainings_ids = trainings_ids[0]

        if trainings_ids is None:
            return Response(data="at least 1 training should be selected", status=status.HTTP_400_BAD_REQUEST)

        serializer = WorkoutSerializer(data=data)
        if serializer.is_valid():
            trainings = [get_object_or_404(Training, pk=training) for training in trainings_ids]

            workout = serializer.save()

            workout.trainings.set(trainings)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        raise InvalidInputFormatException(serializer.errors.items())


@api_view(['GET', 'PUT', 'DELETE'])
@log_handler_decorator(logger)
def workout_detail(request, workout_id):
    """
    GET, UPDATE or DELETE a workout.
    """
    workout = get_object_or_404(Workout, pk=workout_id)

    if request.method == 'GET':
        serializer = WorkoutSerializer(instance=workout)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        data = QueryDict(mutable=True)
        data.update(request.data)
        trainings_ids = data.pop('trainings', None)

        if trainings_ids:
            if isinstance(trainings_ids[0], list):
                trainings_ids = trainings_ids[0]

        serializer = WorkoutSerializer(instance=workout, data=data, partial=True)

        if serializer.is_valid():

            if trainings_ids:
                trainings = [get_object_or_404(Training, id=training) for training in trainings_ids]
                workout.trainings.set(trainings)

            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        raise InvalidInputFormatException(serializer.errors.items())

    if request.method == 'DELETE':
        workout.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
