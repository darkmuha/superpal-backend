from django.contrib.auth import authenticate
from django.http import QueryDict
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from customers.serializers import CustomerSerializer
from utils.custom_exceptions import InvalidInputFormatException
from .models import User
from .serializers import UserSerializer
from .tokens import create_jwt_pair_for_user


# Create your views here.
@api_view(['POST'])
def login_view(request):
    """
    Login view
    """
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
    """
    Signup view (registers customer)
    """
    if request.method == 'POST':
        sign_up_data = request.data

        if sign_up_data.get('is_admin', 'false').lower() == 'true':
            return Response(data="Can't create admin through this route, this is for user registration only",
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomerSerializer(data=sign_up_data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        raise InvalidInputFormatException(serializer.errors.items())


@api_view(['POST'])
def logout_view(request):
    """
    Logout view (adds token to blacklist)
    """

    refresh_token = request.data.get('refresh')

    if refresh_token:
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response(data="Logout Successful", status=status.HTTP_200_OK)
    return Response(data="You are not logged in. refresh_token is required", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_admin(request):
    if request.method == 'POST':
        mutable_data = QueryDict(mutable=True)
        mutable_data.update(request.data)

        mutable_data['is_admin'] = True

        serializer = UserSerializer(data=mutable_data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        raise InvalidInputFormatException(serializer.errors.items())


@api_view(['GET'])
def get_routes(request):
    if request.method == 'GET':
        routes = [
            'authentication/login/',
            'authentication/logout/',
            'authentication/register/',
            'authentication/token/',
            'authentication/token/refresh/',
            'authentication/token/verify/',
            'authentication/create-admin/'
        ]

        return Response(data=routes, status=status.HTTP_200_OK)
