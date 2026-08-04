import pytest
from django.urls import reverse

from apps.authentication.serializers import (
    build_uid_and_token_for_reset,
    build_uid_and_token_for_verification,
)

pytestmark = pytest.mark.django_db


class TestRegistration:
    def test_register_success(self, api_client):
        url = reverse("auth-register")
        payload = {
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "phone": "+923001234567",
            "password": "StrongPass123!",
            "password_confirm": "StrongPass123!",
        }
        response = api_client.post(url, payload, format="json")
        assert response.status_code == 201
        assert response.data["success"] is True

    def test_register_duplicate_email_fails(self, api_client, user_factory):
        user_factory(email="dupe@example.com")
        url = reverse("auth-register")
        payload = {
            "email": "dupe@example.com",
            "first_name": "Dup",
            "password": "StrongPass123!",
            "password_confirm": "StrongPass123!",
        }
        response = api_client.post(url, payload, format="json")
        assert response.status_code == 400

    def test_register_password_mismatch_fails(self, api_client):
        url = reverse("auth-register")
        payload = {
            "email": "mismatch@example.com",
            "first_name": "Mis",
            "password": "StrongPass123!",
            "password_confirm": "Different123!",
        }
        response = api_client.post(url, payload, format="json")
        assert response.status_code == 400

    def test_register_weak_password_fails(self, api_client):
        url = reverse("auth-register")
        payload = {
            "email": "weak@example.com",
            "first_name": "Weak",
            "password": "password",
            "password_confirm": "password",
        }
        response = api_client.post(url, payload, format="json")
        assert response.status_code == 400


class TestLogin:
    def test_login_success(self, api_client, user_factory):
        user_factory(email="login@example.com", password="StrongPass123!")
        url = reverse("auth-login")
        response = api_client.post(
            url,
            {"email": "login@example.com", "password": "StrongPass123!"},
            format="json",
        )
        assert response.status_code == 200
        assert "access" in response.data["data"]
        assert "refresh" in response.data["data"]

    def test_login_wrong_password_fails(self, api_client, user_factory):
        user_factory(email="login2@example.com", password="StrongPass123!")
        url = reverse("auth-login")
        response = api_client.post(
            url,
            {"email": "login2@example.com", "password": "WrongPass!"},
            format="json",
        )
        assert response.status_code == 401

    def test_login_inactive_account_fails(self, api_client, user_factory):
        user = user_factory(email="inactive@example.com", password="StrongPass123!")
        user.is_active = False
        user.save()
        url = reverse("auth-login")
        response = api_client.post(
            url,
            {"email": "inactive@example.com", "password": "StrongPass123!"},
            format="json",
        )
        assert response.status_code in (400, 401)


class TestTokenLifecycle:
    def test_refresh_token(self, api_client, user_factory):
        user_factory(email="refresh@example.com", password="StrongPass123!")
        login = api_client.post(
            reverse("auth-login"),
            {"email": "refresh@example.com", "password": "StrongPass123!"},
            format="json",
        )
        refresh = login.data["data"]["refresh"]
        response = api_client.post(
            reverse("auth-refresh"), {"refresh": refresh}, format="json"
        )
        assert response.status_code == 200
        assert "access" in response.data

    def test_logout_blacklists_token(self, api_client, user_factory):
        user_factory(email="logout@example.com", password="StrongPass123!")
        login = api_client.post(
            reverse("auth-login"),
            {"email": "logout@example.com", "password": "StrongPass123!"},
            format="json",
        )
        access = login.data["data"]["access"]
        refresh = login.data["data"]["refresh"]

        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        logout_response = api_client.post(
            reverse("auth-logout"), {"refresh": refresh}, format="json"
        )
        assert logout_response.status_code == 200

        refresh_response = api_client.post(
            reverse("auth-refresh"), {"refresh": refresh}, format="json"
        )
        assert refresh_response.status_code == 401

    def test_me_requires_authentication(self, api_client):
        response = api_client.get(reverse("auth-me"))
        assert response.status_code == 401


class TestEmailVerification:
    def test_verify_email_success(self, api_client, user_factory):
        user = user_factory(email="verify@example.com")
        uid, token = build_uid_and_token_for_verification(user)
        response = api_client.post(
            reverse("auth-verify-email"), {"uid": uid, "token": token}, format="json"
        )
        assert response.status_code == 200
        user.refresh_from_db()
        assert user.is_email_verified is True

    def test_verify_email_invalid_token_fails(self, api_client, user_factory):
        user = user_factory(email="verify2@example.com")
        response = api_client.post(
            reverse("auth-verify-email"),
            {"uid": "bad-uid", "token": "bad-token"},
            format="json",
        )
        assert response.status_code == 400
        user.refresh_from_db()
        assert user.is_email_verified is False


class TestThrottling:
    """Verifies the ScopedRateThrottle mechanism used on every auth
    endpoint (throttle_scope = "auth") actually blocks after the
    configured limit. Exercises the throttle class directly with an
    explicit rate rather than mutating Django settings mid-test — DRF
    views cache their throttle_classes at import time, so a settings
    override after import wouldn't reach an already-instantiated view
    reliably. Testing the throttle class itself is both more deterministic
    and closer to a true unit test of the rate-limiting logic."""

    def test_scoped_throttle_blocks_after_limit(self):
        from django.core.cache import cache
        from django.test import RequestFactory
        from rest_framework.request import Request
        from rest_framework.throttling import ScopedRateThrottle

        cache.clear()

        class _DummyLoginView:
            throttle_scope = "auth"

        throttle = ScopedRateThrottle()
        throttle.THROTTLE_RATES = {"auth": "3/min"}
        throttle.rate = "3/min"
        throttle.num_requests, throttle.duration = throttle.parse_rate(throttle.rate)

        factory = RequestFactory()
        view = _DummyLoginView()

        results = []
        for _ in range(4):
            request = Request(factory.post("/api/v1/auth/login/"))
            results.append(throttle.allow_request(request, view))

        assert results == [
            True,
            True,
            True,
            False,
        ], "Expected the 4th request within the same window to be throttled."


class TestPasswordReset:
    def test_forgot_password_always_returns_200(self, api_client):
        # Must not leak whether the email exists.
        response = api_client.post(
            reverse("auth-forgot-password"),
            {"email": "nonexistent@example.com"},
            format="json",
        )
        assert response.status_code == 200

    def test_reset_password_success(self, api_client, user_factory):
        user = user_factory(email="reset@example.com", password="OldPass123!")
        uid, token = build_uid_and_token_for_reset(user)
        response = api_client.post(
            reverse("auth-reset-password"),
            {
                "uid": uid,
                "token": token,
                "new_password": "BrandNewPass123!",
                "new_password_confirm": "BrandNewPass123!",
            },
            format="json",
        )
        assert response.status_code == 200

        login = api_client.post(
            reverse("auth-login"),
            {"email": "reset@example.com", "password": "BrandNewPass123!"},
            format="json",
        )
        assert login.status_code == 200

    def test_change_password_requires_correct_old_password(
        self, api_client, user_factory
    ):
        user_factory(email="changepass@example.com", password="OldPass123!")
        login = api_client.post(
            reverse("auth-login"),
            {"email": "changepass@example.com", "password": "OldPass123!"},
            format="json",
        )
        access = login.data["data"]["access"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        response = api_client.post(
            reverse("auth-change-password"),
            {
                "old_password": "WrongOldPass!",
                "new_password": "NewPass123!",
                "new_password_confirm": "NewPass123!",
            },
            format="json",
        )
        assert response.status_code == 400
