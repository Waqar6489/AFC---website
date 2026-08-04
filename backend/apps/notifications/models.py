from django.db import models

from apps.accounts.models import User
from apps.core.models import TimeStampedModel


class Notification(TimeStampedModel):
    """An in-app notification for a user — primarily order status
    updates, but general enough for promos/system messages too."""

    class NotificationType(models.TextChoices):
        ORDER_STATUS = "order_status", "Order Status"
        PROMOTION = "promotion", "Promotion"
        SYSTEM = "system", "System"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    notification_type = models.CharField(
        max_length=15, choices=NotificationType.choices, default=NotificationType.SYSTEM
    )
    title = models.CharField(max_length=150)
    message = models.CharField(max_length=500)
    related_order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
    )
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["user", "is_read"])]

    def __str__(self):
        return f"{self.title} → {self.user.email}"


# Admin notifications are for the admin dashboard, not for users. They can be used to notify admins about new orders, user signups, contact form submissions, etc.
class AdminNotification(TimeStampedModel):

    class NotificationType(models.TextChoices):
        ORDER = "order", "Order"
        USER = "user", "User"
        CONTACT = "contact", "Contact"
        REVIEW = "review", "Review"

    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices
    )

    title = models.CharField(max_length=150)

    message = models.CharField(max_length=500)

    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title    
