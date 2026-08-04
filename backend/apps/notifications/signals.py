"""Automatically creates an in-app Notification whenever an order's
status changes, so the customer's Dashboard > Notifications stays in
sync with the order tracking timeline without any manual wiring at the
call site in apps.orders."""

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.orders.models import OrderStatusHistory

from .models import Notification

_STATUS_MESSAGES = {
    "pending": "Your order has been received and is pending confirmation.",
    "confirmed": "Your order has been confirmed!",
    "preparing": "We've started preparing your order.",
    "cooking": "Your order is being cooked with care.",
    "packing": "Your order is being packed.",
    "ready_for_pickup": "Your order is ready for pickup by our rider.",
    "out_for_delivery": "Your order is out for delivery!",
    "nearby": "Your delivery rider is nearby.",
    "delivered": "Your order has been delivered. Enjoy your meal!",
    "cancelled": "Your order has been cancelled.",
    "refunded": "Your order has been refunded.",
}


@receiver(post_save, sender=OrderStatusHistory)
def create_order_status_notification(sender, instance, created, **kwargs):
    if not created:
        return
    order = instance.order
    Notification.objects.create(
        user=order.user,
        notification_type=Notification.NotificationType.ORDER_STATUS,
        title=f"Order {order.order_number} — {instance.get_status_display()}",
        message=_STATUS_MESSAGES.get(
            instance.status, f"Your order status changed to {instance.status}."
        ),
        related_order=order,
    )
