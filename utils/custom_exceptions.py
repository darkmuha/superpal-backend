from rest_framework import status
from rest_framework.exceptions import APIException

from .serializer_error_message_builder import SerializerErrorMessageBuilder


class BaseCustomException(APIException):
    def __init__(self, detail, code):
        super().__init__(detail, code)
        self.detail = detail
        self.status_code = code


class InvalidInputFormatException(BaseCustomException):
    """
        This constructor processes a list of field-error pairs, identifying required, already been used, and invalid
        fields based on error messages.
        It then formats the information into a single string and initializes the custom exception instance with
        the formatted error message and HTTP status code.
        For now this constructor takes a detail parameter, which represents a list of field-error pairs obtained from the
        serializer.errors.items().
    """

    def __init__(self, detail):
        error_message = InvalidInputFormatException.build_error_message(detail)
        super().__init__(error_message, status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def build_error_message(detail):
        def process_nested_data(data):
            for field, error_list in data:
                error_messages = [str(error) for error in error_list]
                if isinstance(error_list, dict):
                    process_nested_data(error_list.items())
                elif any("This field is required." in error_message for error_message in error_messages):
                    builder.add_required_field(field)
                elif any("already been used" in error_message for error_message in error_messages):
                    builder.add_already_used_field(field)
                else:
                    builder.add_invalid_field(field)

        builder = SerializerErrorMessageBuilder()

        try:
            process_nested_data(detail)
        except TypeError:
            raise ValueError("Invalid input for InvalidInputFormatException: detail must be a dictionary.")

        return builder.build()
