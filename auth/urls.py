from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from auth.views import get_routes, login_view, signup_view, logout_view

urlpatterns = [
    path('', get_routes),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', login_view, name='login'),
    path('register/', signup_view, name='register'),
    path('logout/', logout_view, name='logout')
]
