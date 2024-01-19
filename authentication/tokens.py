from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def create_jwt_pair_for_user(user: User):
    refresh = RefreshToken.for_user(user)

    # Adding custom claim with user email to access token
    access_token = refresh.access_token
    customer = getattr(user, 'customer', None)
    if customer:
        access_token['customer_id'] = str(customer.id)
        refresh['customer_id'] = str(customer.id)

    tokens = {
        "access": str(access_token),
        "refresh": str(refresh)
    }

    return tokens
