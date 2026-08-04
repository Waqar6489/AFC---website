import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestFAQ:
    def test_public_only_sees_active_faqs(self, api_client):
        from apps.faq.models import FAQ

        FAQ.objects.create(question="Active?", answer="Yes", is_active=True)
        FAQ.objects.create(question="Hidden?", answer="No", is_active=False)

        response = api_client.get(reverse("faq-list"))
        questions = [f["question"] for f in response.data["results"]]
        assert "Active?" in questions
        assert "Hidden?" not in questions

    def test_anonymous_cannot_create_faq(self, api_client):
        response = api_client.post(
            reverse("faq-list"), {"question": "Q?", "answer": "A"}
        )
        assert response.status_code in (401, 403)

    def test_admin_can_create_faq(self, api_client, auth_client, user_factory):
        admin = user_factory(email="faqadmin@example.com", role="admin", is_staff=True)
        auth_client(api_client, admin)
        response = api_client.post(
            reverse("faq-list"), {"question": "New Q?", "answer": "New A"}
        )
        assert response.status_code == 201
