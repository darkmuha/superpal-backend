from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError, AuthenticationFailed
from django.core.exceptions import ValidationError

from .constants import exceptions


# This exception is used to edit other Exceptions.
class CustomException(APIException):
    def __init__(self, detail=None, status_code=None):
        if detail is not None:
            self.detail = detail
        if status_code is not None:
            self.status_code = status_code


def custom_exception_handler(exc, con):  # exc = exception, con = context
    # Saved the name(class) of the exception into exception_class
    exception_class = exc.__class__

    if exception_class in exceptions:
        # Setting the status code.
        # This can be done without the CustomException class by just setting status_code in exc.
        custom_exception = CustomException(str(exc), status_code=exceptions[exception_class])
        res = exception_handler(custom_exception, con)

        if exception_class in [InvalidToken, AuthenticationFailed, TokenError]:
            if exception_class == InvalidToken:
                res.data['detail'] = exc.args[0]['detail']
            else:
                res.data['detail'] = exc.args[0]

        res.data = {'error': res.data['detail']}
        return res

    if isinstance(exc, ValidationError):
        error_message = str(exc)[2:-2].replace('“', "'").replace('”', "'")

        custom_exception = CustomException(detail=error_message, status_code=status.HTTP_400_BAD_REQUEST)
        res = exception_handler(custom_exception, con)

        res.data = {'error': res.data['detail']}
        return res

    custom_exception = CustomException(str(exc), status.HTTP_500_INTERNAL_SERVER_ERROR)
    res = exception_handler(custom_exception, con)

    res.data = {'error': res.data['detail']}
    return res
