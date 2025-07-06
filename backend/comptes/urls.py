from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    InscriptionView,
    CustomTokenObtainPairView,
    UserMeView,
)

urlpatterns = [
    # /auth/register/
    path("register/", InscriptionView.as_view(), name="auth_register"),

    # /auth/login/
    path("login/", CustomTokenObtainPairView.as_view(), name="auth_login"),

    # /auth/refresh/
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # /auth/me/
    path("me/", UserMeView.as_view(), name="auth_me"),
]
