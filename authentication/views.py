import logging

from django.contrib.auth import authenticate
from django.http import QueryDict
from django_rest_passwordreset.views import reset_password_confirm
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from customers.serializers import CustomerSerializer
from utils.custom_exceptions import InvalidInputFormatException
from utils.logger_decorator import log_handler_decorator
from .serializers import UserSerializer, MyTokenObtainPairSerializer
from .tokens import create_jwt_pair_for_user

logger = logging.getLogger(__name__)


# Create your views here
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
@log_handler_decorator(logger)
def login_view(request):
    """
    Login view
    """
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user:
            tokens = {
                "tokens": create_jwt_pair_for_user(user)
            }

            return Response(data=tokens, status=status.HTTP_200_OK)
        return Response(data="Invalid email or password", status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@log_handler_decorator(logger)
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
@log_handler_decorator(logger)
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
@log_handler_decorator(logger)
def custom_password_reset_confirm(request):
    if request.method == 'POST':

        token = request.data.get('token', None)

        if not token:
            return Response(data='Token not provided', status=status.HTTP_400_BAD_REQUEST)

        response = reset_password_confirm(request._request, token)

        if response.status_code:
            return Response(data='Token is correct', status=status.HTTP_200_OK)
        else:
            return Response(data='Invalid or expired token', status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@log_handler_decorator(logger)
def create_admin(request):
    if request.method == 'POST':
        mutable_data = QueryDict(mutable=True)
        mutable_data.update(request.data)

        mutable_data['is_admin'] = True
        mutable_data['is_staff'] = True
        mutable_data['is_superuser'] = True

        serializer = UserSerializer(data=mutable_data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        raise InvalidInputFormatException(serializer.errors.items())


@api_view(['GET'])
@log_handler_decorator(logger)
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
