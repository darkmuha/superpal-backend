from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=40)
    email = serializers.EmailField(max_length=255)
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

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)

        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        return user
