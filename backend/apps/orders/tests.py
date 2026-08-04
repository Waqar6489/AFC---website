import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

INSIDE_LAT, INSIDE_LON = 33.7100, 73.0520  # ~0.3km from restaurant fixture
OUTSIDE_LAT, OUTSIDE_LON = 31.5497, 74.3436  # Lahore, ~275km away


class TestCart:
    def test_add_item_and_view_cart(
        self, api_client, auth_client, user_factory, product_factory
    ):
        user = user_factory(email="cart1@example.com")
        auth_client(api_client, user)
        product = product_factory(price=500)

        response = api_client.post(
            reverse("cart-item-list"), {"product": product.id, "quantity": 3}
        )
        assert response.status_code == 201

        cart_response = api_client.get(reverse("cart"))
        assert cart_response.data["subtotal"] == "1500.00"
        assert cart_response.data["item_count"] == 3

    def test_variant_required_if_product_has_variants(
        self, api_client, auth_client, user_factory, product_factory, variant_factory
    ):
        user = user_factory(email="cart2@example.com")
        auth_client(api_client, user)
        product = product_factory()
        variant_factory(product, size="small", price=800)

        response = api_client.post(
            reverse("cart-item-list"), {"product": product.id, "quantity": 1}
        )
        assert response.status_code == 400

    def test_cart_scoped_to_owner(
        self, api_client, auth_client, user_factory, product_factory
    ):
        user_a = user_factory(email="cartowner_a@example.com")
        user_b = user_factory(email="cartowner_b@example.com")
        product = product_factory()

        auth_client(api_client, user_a)
        api_client.post(
            reverse("cart-item-list"), {"product": product.id, "quantity": 1}
        )

        auth_client(api_client, user_b)
        response = api_client.get(reverse("cart-item-list"))
        assert response.data["count"] == 0

    def test_anonymous_cannot_add_to_cart(self, api_client, product_factory):
        product = product_factory()
        response = api_client.post(
            reverse("cart-item-list"), {"product": product.id, "quantity": 1}
        )
        assert response.status_code == 401


class TestDeliveryEligibility:
    def test_inside_radius_allows_delivery(self, api_client, site_config):
        response = api_client.post(
            reverse("check-delivery"), {"latitude": INSIDE_LAT, "longitude": INSIDE_LON}
        )
        assert response.status_code == 200
        assert response.data["data"]["is_within_radius"] is True

    def test_outside_radius_blocks_delivery(self, api_client, site_config):
        response = api_client.post(
            reverse("check-delivery"),
            {"latitude": OUTSIDE_LAT, "longitude": OUTSIDE_LON},
        )
        assert response.status_code == 200
        assert response.data["data"]["is_within_radius"] is False
        assert "10" in response.data["message"]

    def test_invalid_latitude_rejected(self, api_client, site_config):
        response = api_client.post(
            reverse("check-delivery"), {"latitude": 999, "longitude": 73.0}
        )
        assert response.status_code == 400


class TestCheckout:
    def _add_to_cart(self, api_client, product, quantity=1):
        return api_client.post(
            reverse("cart-item-list"), {"product": product.id, "quantity": quantity}
        )

    def test_checkout_blocked_outside_radius(
        self, api_client, auth_client, user_factory, product_factory, site_config
    ):
        user = user_factory(email="checkout1@example.com")
        auth_client(api_client, user)
        product = product_factory(price=1000)
        self._add_to_cart(api_client, product)

        response = api_client.post(
            reverse("checkout"),
            {
                "full_name": "Test Buyer",
                "phone": "+923001234567",
                "address_line": "Somewhere",
                "city": "Lahore",
                "latitude": OUTSIDE_LAT,
                "longitude": OUTSIDE_LON,
                "payment_method": "cod",
            },
            format="json",
        )
        assert response.status_code == 400
        assert "10.00 KM" in str(response.data)

    def test_checkout_succeeds_inside_radius(
        self, api_client, auth_client, user_factory, product_factory, site_config
    ):
        user = user_factory(email="checkout2@example.com")
        auth_client(api_client, user)
        product = product_factory(price=1000, stock=10)
        self._add_to_cart(api_client, product, quantity=2)

        response = api_client.post(
            reverse("checkout"),
            {
                "full_name": "Test Buyer",
                "phone": "+923001234567",
                "address_line": "F-8 Markaz",
                "city": "Islamabad",
                "latitude": INSIDE_LAT,
                "longitude": INSIDE_LON,
                "payment_method": "cod",
            },
            format="json",
        )
        assert response.status_code == 201
        assert response.data["data"]["subtotal"] == "2000.00"
        assert response.data["data"]["status"] == "pending"

        product.refresh_from_db()
        assert product.stock == 8  # decremented by quantity ordered

        cart_response = api_client.get(reverse("cart"))
        assert cart_response.data["item_count"] == 0

    def test_checkout_fails_with_empty_cart(
        self, api_client, auth_client, user_factory, site_config
    ):
        user = user_factory(email="checkout3@example.com")
        auth_client(api_client, user)
        response = api_client.post(
            reverse("checkout"),
            {
                "full_name": "Test Buyer",
                "phone": "+923001234567",
                "address_line": "F-8 Markaz",
                "city": "Islamabad",
                "latitude": INSIDE_LAT,
                "longitude": INSIDE_LON,
                "payment_method": "cod",
            },
            format="json",
        )
        assert response.status_code == 400

    def test_checkout_fails_insufficient_stock(
        self, api_client, auth_client, user_factory, product_factory, site_config
    ):
        user = user_factory(email="checkout4@example.com")
        auth_client(api_client, user)
        product = product_factory(price=1000, stock=1)
        self._add_to_cart(api_client, product, quantity=5)

        response = api_client.post(
            reverse("checkout"),
            {
                "full_name": "Test Buyer",
                "phone": "+923001234567",
                "address_line": "F-8 Markaz",
                "city": "Islamabad",
                "latitude": INSIDE_LAT,
                "longitude": INSIDE_LON,
                "payment_method": "cod",
            },
            format="json",
        )
        assert response.status_code == 400
        assert "stock" in str(response.data).lower()

    def test_checkout_with_valid_coupon_applies_discount(
        self, api_client, auth_client, user_factory, product_factory, site_config
    ):
        from datetime import timedelta

        from django.utils import timezone

        from apps.deals.models import Deal

        Deal.objects.create(
            title="Test Deal",
            discount_type="percentage",
            discount_value=10,
            min_order_amount=100,
            coupon_code="TEST10",
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1),
        )

        user = user_factory(email="checkout5@example.com")
        auth_client(api_client, user)
        product = product_factory(price=1000, stock=10)
        self._add_to_cart(api_client, product)

        response = api_client.post(
            reverse("checkout"),
            {
                "full_name": "Test Buyer",
                "phone": "+923001234567",
                "address_line": "F-8 Markaz",
                "city": "Islamabad",
                "latitude": INSIDE_LAT,
                "longitude": INSIDE_LON,
                "payment_method": "cod",
                "coupon_code": "test10",
            },
            format="json",
        )
        assert response.status_code == 201
        assert response.data["data"]["discount_amount"] == "100.00"
        assert response.data["data"]["total_amount"] == "900.00"


class TestOrderOwnership:
    def test_customer_only_sees_own_orders(
        self, api_client, auth_client, user_factory, product_factory, site_config
    ):
        user_a = user_factory(email="ordera@example.com")
        user_b = user_factory(email="orderb@example.com")
        product = product_factory(price=500, stock=10)

        auth_client(api_client, user_a)
        api_client.post(
            reverse("cart-item-list"), {"product": product.id, "quantity": 1}
        )
        api_client.post(
            reverse("checkout"),
            {
                "full_name": "A",
                "phone": "+923001234567",
                "address_line": "St",
                "city": "Islamabad",
                "latitude": INSIDE_LAT,
                "longitude": INSIDE_LON,
                "payment_method": "cod",
            },
            format="json",
        )

        auth_client(api_client, user_b)
        response = api_client.get(reverse("order-list"))
        assert response.data["count"] == 0

    def test_non_admin_cannot_update_order_status(
        self, api_client, auth_client, user_factory, product_factory, site_config
    ):
        user = user_factory(email="orderc@example.com")
        auth_client(api_client, user)
        product = product_factory(price=500, stock=10)
        api_client.post(
            reverse("cart-item-list"), {"product": product.id, "quantity": 1}
        )
        checkout_response = api_client.post(
            reverse("checkout"),
            {
                "full_name": "A",
                "phone": "+923001234567",
                "address_line": "St",
                "city": "Islamabad",
                "latitude": INSIDE_LAT,
                "longitude": INSIDE_LON,
                "payment_method": "cod",
            },
            format="json",
        )
        order_number = checkout_response.data["data"]["order_number"]

        response = api_client.post(
            reverse("order-update-status", kwargs={"order_number": order_number}),
            {"status": "confirmed"},
        )
        assert response.status_code == 403
