from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from authentication.views import get_routes, login_view, signup_view, logout_view, create_admin

urlpatterns = [
    path('', get_routes, name='get-routes'),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('login/', login_view, name='login'),  # login
    path('register/', signup_view, name='register'),  # create customer
    path('logout/', logout_view, name='logout'),  # logout
    path('create-admin/', create_admin, name='create-admin'),  # create admin user
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
