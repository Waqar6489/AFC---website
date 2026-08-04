from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from apps.deals.models import Deal

pytestmark = pytest.mark.django_db


def _make_deal(**overrides):
    defaults = dict(
        title="Test Deal",
        discount_type="percentage",
        discount_value=10,
        min_order_amount=100,
        coupon_code="SAVE10",
        start_date=timezone.now() - timedelta(days=1),
        end_date=timezone.now() + timedelta(days=1),
    )
    defaults.update(overrides)
    return Deal.objects.create(**defaults)


class TestDealStatus:
    def test_active_deal_status(self):
        deal = _make_deal()
        assert deal.status == Deal.Status.ACTIVE
        assert deal.is_currently_active is True

    def test_scheduled_deal_status(self):
        deal = _make_deal(
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=5),
        )
        assert deal.status == Deal.Status.SCHEDULED

    def test_expired_deal_status(self):
        deal = _make_deal(
            start_date=timezone.now() - timedelta(days=5),
            end_date=timezone.now() - timedelta(days=1),
        )
        assert deal.status == Deal.Status.EXPIRED

    def test_disabled_deal_status(self):
        deal = _make_deal(is_active=False)
        assert deal.status == Deal.Status.DISABLED

    def test_percentage_discount_calculation(self):
        deal = _make_deal(discount_type="percentage", discount_value=20)
        assert deal.calculate_discount(1000) == 200

    def test_percentage_discount_respects_cap(self):
        deal = _make_deal(
            discount_type="percentage", discount_value=50, max_discount_amount=100
        )
        assert deal.calculate_discount(1000) == 100

    def test_fixed_discount_never_exceeds_order_amount(self):
        deal = _make_deal(discount_type="fixed", discount_value=500)
        assert deal.calculate_discount(200) == 200


class TestCouponValidateEndpoint:
    def test_valid_coupon(self, api_client):
        _make_deal()
        response = api_client.post(
            reverse("validate-coupon"),
            {"code": "SAVE10", "order_amount": 1000},
            format="json",
        )
        assert response.status_code == 200
        assert response.data["data"]["discount_amount"] == 100

    def test_invalid_coupon_code(self, api_client):
        response = api_client.post(
            reverse("validate-coupon"),
            {"code": "NOPE", "order_amount": 1000},
            format="json",
        )
        assert response.status_code == 400

    def test_below_minimum_order_amount(self, api_client):
        _make_deal(min_order_amount=500)
        response = api_client.post(
            reverse("validate-coupon"),
            {"code": "SAVE10", "order_amount": 100},
            format="json",
        )
        assert response.status_code == 400

    def test_expired_coupon_rejected(self, api_client):
        _make_deal(
            start_date=timezone.now() - timedelta(days=10),
            end_date=timezone.now() - timedelta(days=1),
        )
        response = api_client.post(
            reverse("validate-coupon"),
            {"code": "SAVE10", "order_amount": 1000},
            format="json",
        )
        assert response.status_code == 400


class TestDealListing:
    def test_active_endpoint_only_returns_currently_running_deals(self, api_client):
        _make_deal(title="Running", coupon_code="RUN1")
        _make_deal(
            title="Expired",
            coupon_code="EXP1",
            start_date=timezone.now() - timedelta(days=10),
            end_date=timezone.now() - timedelta(days=1),
        )
        response = api_client.get(reverse("deal-active"))
        titles = [d["title"] for d in response.data]
        assert "Running" in titles
        assert "Expired" not in titles
