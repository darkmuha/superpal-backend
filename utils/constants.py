from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.exceptions import (
    ParseError,
    NotAuthenticated,
    PermissionDenied,
    NotFound,
    MethodNotAllowed,
    NotAcceptable,
    UnsupportedMediaType,
    Throttled
)
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError, AuthenticationFailed

from .custom_exceptions import InvalidInputFormatException

# Dictionary of what status code to return for each error
exceptions = {
    InvalidInputFormatException: status.HTTP_400_BAD_REQUEST,
    ParseError: status.HTTP_400_BAD_REQUEST,
    ValueError: status.HTTP_400_BAD_REQUEST,
    AuthenticationFailed: status.HTTP_401_UNAUTHORIZED,
    InvalidToken: status.HTTP_401_UNAUTHORIZED,
    NotAuthenticated: status.HTTP_401_UNAUTHORIZED,
    TokenError: status.HTTP_401_UNAUTHORIZED,
    PermissionDenied: status.HTTP_403_FORBIDDEN,
    Http404: status.HTTP_404_NOT_FOUND,
    NotFound: status.HTTP_404_NOT_FOUND,
    ObjectDoesNotExist: status.HTTP_404_NOT_FOUND,
    MethodNotAllowed: status.HTTP_405_METHOD_NOT_ALLOWED,
    NotAcceptable: status.HTTP_406_NOT_ACCEPTABLE,
    UnsupportedMediaType: status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    Throttled: status.HTTP_429_TOO_MANY_REQUESTS,

}
