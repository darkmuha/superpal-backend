from rest_framework import serializers

from authentication.serializers import UserSerializer
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
        }
        representation['user'] = user_representation
        return representation

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
        else:
            raise serializers.ValidationError(user_serializer.errors)

        customer = Customer.objects.create(user=user, **validated_data)
        return customer
