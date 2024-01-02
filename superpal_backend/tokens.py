from django_rest_passwordreset.tokens import BaseTokenGenerator
import secrets
import string


class CustomTokenGenerator(BaseTokenGenerator):
    """
    Generates a random string with length using secrets.choice between ascii letters and digits
    """

    def __init__(self, *args, **kwargs):
        self.length = kwargs.get('length', 6)

    def generate_token(self, *args, **kwargs):
        token = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(self.length))

        return token
