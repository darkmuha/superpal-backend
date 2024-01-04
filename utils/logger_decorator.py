import functools
from rest_framework import status


def log_handler_decorator(logger):
    def decorator(func):
        # this method disables default wrapper functionality.
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            logger.info("Received request: %s",
                        {"method": request.method,
                         "url": request.build_absolute_uri(),
                         "headers": dict(request.headers),
                         "body": sanitize_sensitive_data(request.data)})

            response = func(request, *args, **kwargs)

            if response.status_code >= 400 or not response.status_code:
                logger.warning("Returning response: %s", {
                    "status_code":
                        response.status_code if response.status_code else status.HTTP_400_BAD_REQUEST
                })
            else:
                logger.info("Returning response: %s",
                            {"status_code": response.status_code})

            return response

        return wrapper

    return decorator


def sanitize_sensitive_data(data):
    def sanitize_recursive(d):
        if isinstance(d, dict):
            return {key: sanitize_recursive(value) if key != 'password' else '********' for key, value in d.items()}
        elif isinstance(d, list):
            return [sanitize_recursive(item) for item in d]
        else:
            return d

    return sanitize_recursive(data)
