from rest_framework import serializers

from authentication.serializers import UserSerializer
from utils.custom_exceptions import InvalidInputFormatException
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

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
