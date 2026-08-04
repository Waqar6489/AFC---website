import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestContactMessage:
    def test_public_can_submit_message(self, api_client):
        response = api_client.post(
            reverse("contact-submit"),
            {
                "name": "Bilal",
                "email": "bilal@example.com",
                "subject": "Enquiry",
                "message": "Can I order in bulk?",
            },
        )
        assert response.status_code == 201
        assert response.data["success"] is True

    def test_non_admin_cannot_list_messages(
        self, api_client, auth_client, user_factory
    ):
        user = user_factory(email="notadmin@example.com")
        auth_client(api_client, user)
        response = api_client.get(reverse("contact-message-admin-list"))
        assert response.status_code == 403

    def test_admin_can_list_and_resolve_messages(
        self, api_client, auth_client, user_factory
    ):
        from apps.contact.models import ContactMessage

        message = ContactMessage.objects.create(
            name="Ali", email="ali@example.com", subject="X", message="Y"
        )
        admin = user_factory(
            email="contactadmin@example.com", role="admin", is_staff=True
        )
        auth_client(api_client, admin)

        list_response = api_client.get(reverse("contact-message-admin-list"))
        assert list_response.data["count"] == 1

        patch_response = api_client.patch(
            reverse("contact-message-admin-detail", kwargs={"pk": message.pk}),
            {"admin_reply": "We'll call you shortly.", "is_resolved": True},
            format="json",
        )
        assert patch_response.status_code == 200
        message.refresh_from_db()
        assert message.is_resolved is True
        assert message.replied_by == admin


class TestNewsletter:
    def test_subscribe_success(self, api_client):
        response = api_client.post(
            reverse("newsletter-subscribe"), {"email": "new@example.com"}
        )
        assert response.status_code == 201

    def test_duplicate_subscribe_rejected(self, api_client):
        from apps.contact.models import NewsletterSubscriber

        NewsletterSubscriber.objects.create(
            email="existing@example.com", is_active=True
        )
        response = api_client.post(
            reverse("newsletter-subscribe"), {"email": "existing@example.com"}
        )
        assert response.status_code == 400
