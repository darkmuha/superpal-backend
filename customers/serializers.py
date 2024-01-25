from rest_framework import serializers

from authentication.serializers import UserSerializer
from utils.custom_exceptions import InvalidInputFormatException
from .models import Customer, Progress


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    rank_named = serializers.CharField(source='get_rank_display', read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_representation = {
            'id': instance.user.id,
            'username': instance.user.username,
            'email': instance.user.email,
        }
        representation['user'] = user_representation
        return representation

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        user_serializer = UserSerializer(data=user_data)

        if not user_serializer.is_valid():
            raise InvalidInputFormatException(user_serializer.errors.items())

        user = user_serializer.save()

        customer = Customer.objects.create(user=user, **validated_data)
        return customer

    def update(self, instance, validated_data):
        # Update nested serializer
        user_data = validated_data.pop('user', {})
        user_instance = instance.user
        user_serializer = UserSerializer(instance=user_instance, data=user_data, partial=True)

        if user_serializer.is_valid():
            user_serializer.save()

        super().update(instance, validated_data)

        return instance


class SortedCustomerSerializer(serializers.ModelSerializer):
    rank = serializers.CharField(source='get_rank_display', read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'age', 'workout_streak', 'rank', 'profile_picture', 'current_gym', 'birthdate']


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = '__all__'
