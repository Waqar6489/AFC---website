import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def _create_order(user):
    from apps.orders.models import Order

    return Order.objects.create(
        user=user,
        delivery_full_name="T",
        delivery_phone="+923001234567",
        delivery_address_line="St",
        delivery_city="Islamabad",
        delivery_latitude=33.7077,
        delivery_longitude=73.0498,
        distance_km=0.1,
        subtotal=500,
        total_amount=500,
    )


class TestNotificationSignal:
    def test_order_status_change_creates_notification(self, user_factory):
        from apps.notifications.models import Notification
        from apps.orders.models import Order, OrderStatusHistory

        user = user_factory(email="notifuser@example.com")
        order = _create_order(user)

        OrderStatusHistory.objects.create(
            order=order, status=Order.Status.CONFIRMED, note="Confirmed."
        )

        notifications = Notification.objects.filter(user=user)
        assert notifications.count() == 1
        assert notifications.first().related_order == order
        assert "Confirmed" in notifications.first().title


class TestNotificationEndpoints:
    def test_user_only_sees_own_notifications(
        self, api_client, auth_client, user_factory
    ):
        from apps.orders.models import Order, OrderStatusHistory

        user_a = user_factory(email="notifa@example.com")
        user_b = user_factory(email="notifb@example.com")
        order = _create_order(user_a)
        OrderStatusHistory.objects.create(order=order, status=Order.Status.CONFIRMED)

        auth_client(api_client, user_b)
        response = api_client.get(reverse("notification-list"))
        assert response.data["count"] == 0

        auth_client(api_client, user_a)
        response = api_client.get(reverse("notification-list"))
        assert response.data["count"] == 1

    def test_mark_read_and_unread_count(self, api_client, auth_client, user_factory):
        from apps.orders.models import Order, OrderStatusHistory

        user = user_factory(email="notifc@example.com")
        order = _create_order(user)
        OrderStatusHistory.objects.create(order=order, status=Order.Status.CONFIRMED)
        OrderStatusHistory.objects.create(order=order, status=Order.Status.PREPARING)

        auth_client(api_client, user)
        unread_response = api_client.get(reverse("notification-unread-count"))
        assert unread_response.data["data"]["unread_count"] == 2

        list_response = api_client.get(reverse("notification-list"))
        first_id = list_response.data["results"][0]["id"]
        api_client.post(reverse("notification-mark-read", kwargs={"pk": first_id}))

        unread_after = api_client.get(reverse("notification-unread-count"))
        assert unread_after.data["data"]["unread_count"] == 1

        api_client.post(reverse("notification-mark-all-read"))
        final_unread = api_client.get(reverse("notification-unread-count"))
        assert final_unread.data["data"]["unread_count"] == 0
