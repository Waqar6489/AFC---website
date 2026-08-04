from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.notifications.models import AdminNotification
from apps.accounts.models import User
from apps.core.utils import send_templated_email

from .serializers import (
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    ForgotPasswordSerializer,
    LogoutSerializer,
    RegisterSerializer,
    ResendVerificationEmailSerializer,
    ResetPasswordConfirmSerializer,
    VerifyEmailSerializer,
    build_uid_and_token_for_reset,
    build_uid_and_token_for_verification,
)


def _send_verification_email(user):
    uid, token = build_uid_and_token_for_verification(user)
    verification_link = f"{settings.FRONTEND_URL}/verify-email?uid={uid}&token={token}"
    send_templated_email(
        subject="Verify your AFC - Ahmad Foods account",
        template_name="emails/verify_email.html",
        context={"first_name": user.first_name, "verification_link": verification_link},
        to_email=user.email,
    )


class RegisterView(generics.CreateAPIView):
    """Public registration endpoint. Creates the account, then sends a
    verification email; the account can log in immediately but should be
    nudged in the UI to verify its email (is_email_verified is returned
    on login and in the JWT claims)."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_scope = "auth"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        AdminNotification.objects.create(
        notification_type=AdminNotification.NotificationType.USER,
        title="New User Registration",
        message=f"{user.get_full_name() or user.email} created a new account.",)

        _send_verification_email(user)
        return Response(
            {
                "success": True,
                "message": "Account created successfully. Please check your email to verify your account.",
                "data": {"id": str(user.id), "email": user.email},
            },
            status=status.HTTP_201_CREATED,
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    """Login endpoint — issues an access + refresh JWT pair with custom
    claims (role, verification status, full name)."""

    serializer_class = CustomTokenObtainPairSerializer
    throttle_scope = "auth"

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            response.data = {
                "success": True,
                "message": "Login successful.",
                "data": response.data,
            }
        return response


class LogoutView(APIView):
    """Blacklists the supplied refresh token so it can no longer be used
    to obtain new access tokens — a proper server-side logout rather than
    just deleting the token client-side."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            token = RefreshToken(serializer.validated_data["refresh"])
            token.blacklist()
        except TokenError:
            return Response(
                {
                    "success": False,
                    "message": "Invalid or already-expired token.",
                    "errors": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"success": True, "message": "Logged out successfully.", "errors": {}},
            status=status.HTTP_200_OK,
        )


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        print(request.data)

        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = serializer.save()

        print(result)

        return Response({
            "success": True,
            "message": "Email verified successfully.",
            "data": {
                "access": result["access"],
                "refresh": result["refresh"],
                "user": {
                    "id": str(result["user"].id),
                    "email": result["user"].email,
                    "full_name": result["user"].get_full_name(),
                    "role": result["user"].role,
                    "is_email_verified": True,
                },
            },
        })

class ResendVerificationEmailView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "auth"

    def post(self, request):
        serializer = ResendVerificationEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        # Always return the same response whether or not the account
        # exists / is already verified — prevents email enumeration.
        user = User.objects.filter(email__iexact=email, is_email_verified=False).first()
        if user:
            _send_verification_email(user)

        return Response(
            {
                "success": True,
                "message": "If an unverified account exists with this email, a verification link has been sent.",
                "errors": {},
            },
            status=status.HTTP_200_OK,
        )


class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "password_reset"

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        user = User.objects.filter(email__iexact=email).first()
        if user:
            uid, token = build_uid_and_token_for_reset(user)
            reset_link = (
                f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}"
            )
            send_templated_email(
                subject="Reset your AFC - Ahmad Foods password",
                template_name="emails/reset_password.html",
                context={"first_name": user.first_name, "reset_link": reset_link},
                to_email=user.email,
            )

        # Always the same response — prevents email enumeration.
        return Response(
            {
                "success": True,
                "message": "If an account exists with this email, a password reset link has been sent.",
                "errors": {},
            },
            status=status.HTTP_200_OK,
        )


class ResetPasswordConfirmView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "password_reset"

    def post(self, request):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": True,
                "message": "Password reset successfully. You can now log in.",
                "errors": {},
            },
            status=status.HTTP_200_OK,
        )


class ChangePasswordView(APIView):
    """Authenticated endpoint for a logged-in user to change their own
    password (requires the current password)."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": True,
                "message": "Password changed successfully.",
                "errors": {},
            },
            status=status.HTTP_200_OK,
        )


class MeView(APIView):
    """Quick endpoint the frontend can call on app load to check whether
    the current access token is still valid and get basic identity info."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                "success": True,
                "message": "",
                "data": {
                    "id": str(user.id),
                    "email": user.email,
                    "full_name": user.get_full_name(),
                    "role": user.role,
                    "is_email_verified": user.is_email_verified,
                },
            },
            status=status.HTTP_200_OK,
        )
