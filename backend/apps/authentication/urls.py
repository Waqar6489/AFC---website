from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    ChangePasswordView,
    CustomTokenObtainPairView,
    ForgotPasswordView,
    LogoutView,
    MeView,
    RegisterView,
    ResendVerificationEmailView,
    ResetPasswordConfirmView,
    VerifyEmailView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="auth-login"),
    path("refresh/", TokenRefreshView.as_view(), name="auth-refresh"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("me/", MeView.as_view(), name="auth-me"),
    path("verify-email/", VerifyEmailView.as_view(), name="auth-verify-email"),
    path(
        "resend-verification/",
        ResendVerificationEmailView.as_view(),
        name="auth-resend-verification",
    ),
    path("forgot-password/", ForgotPasswordView.as_view(), name="auth-forgot-password"),
    path(
        "reset-password/",
        ResetPasswordConfirmView.as_view(),
        name="auth-reset-password",
    ),
    path("change-password/", ChangePasswordView.as_view(), name="auth-change-password"),
]
