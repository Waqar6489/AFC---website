import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestHaversine:
    def test_zero_distance_for_same_point(self):
        from apps.core.geo import haversine_distance_km

        assert haversine_distance_km(33.7077, 73.0498, 33.7077, 73.0498) == 0

    def test_known_distance_approximation(self):
        from apps.core.geo import haversine_distance_km

        # Islamabad to Lahore is roughly 275 km as the crow flies.
        distance = haversine_distance_km(33.6844, 73.0479, 31.5497, 74.3436)
        assert 260 < distance < 290

    def test_is_within_delivery_radius(self):
        from apps.core.geo import is_within_delivery_radius

        within, distance = is_within_delivery_radius(
            33.7100, 73.0520, 33.7077, 73.0498, 10
        )
        assert within is True
        assert distance < 10

        within, distance = is_within_delivery_radius(
            31.5497, 74.3436, 33.7077, 73.0498, 10
        )
        assert within is False


class TestAdminAnalytics:
    def test_requires_admin_role(self, api_client, auth_client, user_factory):
        user = user_factory(email="notadmin2@example.com")
        auth_client(api_client, user)
        response = api_client.get(reverse("admin-analytics"))
        assert response.status_code == 403

    def test_admin_can_access_analytics(
        self, api_client, auth_client, user_factory, product_factory
    ):
        admin = user_factory(
            email="analyticsadmin@example.com", role="admin", is_staff=True
        )
        product_factory()
        auth_client(api_client, admin)
        response = api_client.get(reverse("admin-analytics"))
        assert response.status_code == 200
        assert "revenue" in response.data["data"]
        assert response.data["data"]["products"]["total"] == 1

    def test_anonymous_cannot_access_analytics(self, api_client):
        response = api_client.get(reverse("admin-analytics"))
        assert response.status_code == 401


class TestSiteConfiguration:
    def test_load_creates_singleton_with_defaults(self, db):
        from apps.core.models import SiteConfiguration

        config = SiteConfiguration.load()
        assert config.pk == 1
        second = SiteConfiguration.load()
        assert second.pk == config.pk

    def test_singleton_cannot_be_deleted(self, db):
        from apps.core.models import SiteConfiguration

        config = SiteConfiguration.load()
        config.delete()
        assert SiteConfiguration.objects.filter(pk=1).exists()

    def test_public_site_config_endpoint(self, api_client, db):
        from apps.core.models import SiteConfiguration

        config = SiteConfiguration.load()
        config.contact_phone = "+923001234567"
        config.save()

        response = api_client.get(reverse("site-config"))
        assert response.status_code == 200
        assert response.data["data"]["contact_phone"] == "+923001234567"
        assert "maintenance_mode" not in response.data["data"]
