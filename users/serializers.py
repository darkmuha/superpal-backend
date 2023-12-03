from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, Customer


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=40)
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(min_length=8, write_only=True)
    is_admin = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')

        if email and User.objects.filter(email=email).exists():
            raise ValidationError({'email': 'Email has already been used'})

        if username and User.objects.filter(username=username).exists():
            raise ValidationError({'username': 'Username has already been used'})

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")
        is_admin = validated_data.pop("is_admin")
        user = super().create(validated_data)
        user.set_password(password)
        user.is_admin = is_admin
        user.save()
        return user


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
