from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserSerializer, CustomerSerializer
from .tokens import create_jwt_pair_for_user


# Create your views here.
@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user:
            tokens = create_jwt_pair_for_user(user)

            return Response(data=tokens, status=status.HTTP_200_OK)
        return Response(data="Invalid email or password", status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def signup_view(request):
    if request.method == 'POST':
        sign_up_data = request.data

        if "is_admin" in sign_up_data:
            del sign_up_data["is_admin"]

        serializer = CustomerSerializer(data=sign_up_data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_view(request):
    """
    Logout view (adds token to blacklist)
    """

    refresh_token = request.data.get('refresh_token')

    if refresh_token:
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response(data="Logout Successful", status=status.HTTP_200_OK)
    return Response(data="You are not logged in. Refresh token is required", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_routes(request):
    if request.method == 'GET':
        routes = [
            'auth/login/',
            'auth/logout',
            'auth/register',
            'auth/token/',
            'auth/token/refresh'
        ]

        return Response(data=routes, status=status.HTTP_200_OK)
