from django.db.models import Q
from rest_framework import serializers

from customers.models import Customer
from superpals.models import SuperPals, SuperPalWorkoutRequest
from utils.enums import SuperPalWorkoutRequestStatus


class SuperPalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperPals
        fields = '__all__'


class SuperPalWorkoutRequestSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all())
    recipient = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all())

    class Meta:
        model = SuperPalWorkoutRequest
        fields = '__all__'

    def validate(self, data):
        sender = data.get('sender', None)
        recipient = data.get('recipient', None)
        if self.instance is None:
            if sender == recipient:
                raise serializers.ValidationError("Sender and recipient cannot be the same user.")

        if SuperPalWorkoutRequest.objects.filter(
                (Q(sender=sender, recipient=recipient,
                   status__in=[SuperPalWorkoutRequestStatus.PENDING, SuperPalWorkoutRequestStatus.ACCEPTED]) |
                 Q(sender=recipient, recipient=sender,
                   status__in=[SuperPalWorkoutRequestStatus.PENDING, SuperPalWorkoutRequestStatus.ACCEPTED]))
        ).exists():
            raise serializers.ValidationError("Duplicate pair of sender and recipient is not allowed.")

        return data

    def update(self, instance, validated_data):
        validated_data.pop('sender', None)
        validated_data.pop('recipient', None)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        sender_representation = {
            'id': instance.sender.id,
            'username': instance.sender.user.username,
            'email': instance.sender.user.email,
        }
        representation['sender'] = sender_representation
        recipient_representation = {
            'id': instance.recipient.id,
            'username': instance.recipient.user.username,
            'email': instance.recipient.user.email,
        }
        representation['recipient'] = recipient_representation

        return representation
