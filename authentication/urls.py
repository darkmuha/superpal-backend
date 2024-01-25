from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from authentication.views import get_routes, login_view, signup_view, logout_view, create_admin, \
    custom_password_reset_confirm
from .views import MyTokenObtainPairView

urlpatterns = [
    path('', get_routes, name='get-routes'),
    path('token/', MyTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('login/', login_view, name='login'),  # login
    path('register/', signup_view, name='register'),  # create customer
    path('logout/', logout_view, name='logout'),  # logout
    path('create-admin/', create_admin, name='create-admin'),  # create admin user
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('password_reset/confirm-token/', custom_password_reset_confirm, name='password_reset_confirm'),

]
