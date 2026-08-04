import pytest
from django.urls import reverse

from apps.orders.models import Order

pytestmark = pytest.mark.django_db


def _create_delivered_order(user, product, quantity=1):
    from apps.orders.models import OrderItem

    order = Order.objects.create(
        user=user,
        delivery_full_name="Test",
        delivery_phone="+923001234567",
        delivery_address_line="St",
        delivery_city="Islamabad",
        delivery_latitude=33.7077,
        delivery_longitude=73.0498,
        distance_km=0.1,
        subtotal=product.price * quantity,
        total_amount=product.price * quantity,
        status=Order.Status.DELIVERED,
    )
    OrderItem.objects.create(
        order=order,
        product=product,
        product_name=product.name,
        unit_price=product.price,
        quantity=quantity,
        line_total=product.price * quantity,
    )
    return order


class TestReviewCreation:
    def test_verified_buyer_can_review(
        self, api_client, auth_client, user_factory, product_factory
    ):
        user = user_factory(email="reviewer1@example.com")
        product = product_factory()
        _create_delivered_order(user, product)
        auth_client(api_client, user)

        response = api_client.post(
            reverse("review-list"),
            {"product": product.id, "rating": 5, "comment": "Great!"},
        )
        assert response.status_code == 201
        assert response.data["is_verified_purchase"] is True
        assert response.data["is_approved"] is False  # always requires admin approval

    def test_non_buyer_cannot_review(
        self, api_client, auth_client, user_factory, product_factory
    ):
        user = user_factory(email="reviewer2@example.com")
        product = product_factory()
        auth_client(api_client, user)

        response = api_client.post(
            reverse("review-list"),
            {"product": product.id, "rating": 5, "comment": "Never bought this"},
        )
        assert response.status_code == 400

    def test_pending_order_cannot_review_yet(
        self, api_client, auth_client, user_factory, product_factory
    ):
        from apps.orders.models import OrderItem

        user = user_factory(email="reviewer3@example.com")
        product = product_factory()
        order = Order.objects.create(
            user=user,
            delivery_full_name="T",
            delivery_phone="+923001234567",
            delivery_address_line="St",
            delivery_city="Islamabad",
            delivery_latitude=33.7077,
            delivery_longitude=73.0498,
            distance_km=0.1,
            subtotal=product.price,
            total_amount=product.price,
            status=Order.Status.PENDING,
        )
        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            unit_price=product.price,
            quantity=1,
            line_total=product.price,
        )

        auth_client(api_client, user)
        response = api_client.post(
            reverse("review-list"),
            {"product": product.id, "rating": 5, "comment": "Too early"},
        )
        assert response.status_code == 400

    def test_cannot_double_review_same_order(
        self, api_client, auth_client, user_factory, product_factory
    ):
        user = user_factory(email="reviewer4@example.com")
        product = product_factory()
        _create_delivered_order(user, product)
        auth_client(api_client, user)

        first = api_client.post(
            reverse("review-list"),
            {"product": product.id, "rating": 5, "comment": "First"},
        )
        assert first.status_code == 201
        second = api_client.post(
            reverse("review-list"),
            {"product": product.id, "rating": 4, "comment": "Second"},
        )
        assert second.status_code == 400

    def test_anonymous_cannot_review(self, api_client, product_factory):
        product = product_factory()
        response = api_client.post(
            reverse("review-list"), {"product": product.id, "rating": 5, "comment": "x"}
        )
        assert response.status_code == 401


class TestReviewVisibility:
    def test_unapproved_review_hidden_from_public(
        self, api_client, auth_client, user_factory, product_factory
    ):
        user = user_factory(email="reviewer5@example.com")
        product = product_factory()
        _create_delivered_order(user, product)
        auth_client(api_client, user)
        api_client.post(
            reverse("review-list"),
            {"product": product.id, "rating": 5, "comment": "Pending approval"},
        )

        anon_client = api_client
        anon_client.credentials()  # clear auth
        response = anon_client.get(reverse("review-list"), {"product": product.id})
        assert response.data["count"] == 0

    def test_approved_review_visible_to_public_and_updates_product_rating(
        self, api_client, auth_client, user_factory, product_factory
    ):
        from apps.reviews.models import Review

        user = user_factory(email="reviewer6@example.com")
        product = product_factory()
        _create_delivered_order(user, product)
        auth_client(api_client, user)
        create_response = api_client.post(
            reverse("review-list"),
            {"product": product.id, "rating": 4, "comment": "Nice"},
        )

        review = Review.objects.get(pk=create_response.data["id"])
        review.is_approved = True
        review.save()

        product.refresh_from_db()
        assert product.review_count == 1
        assert float(product.average_rating) == 4.0

        api_client.credentials()
        response = api_client.get(reverse("review-list"), {"product": product.id})
        assert response.data["count"] == 1
