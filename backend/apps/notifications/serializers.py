from rest_framework import serializers

from .models import Notification
from .models import AdminNotification

class NotificationSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(
        source="related_order.order_number", read_only=True, default=None
    )

    class Meta:
        model = Notification
        fields = [
            "id",
            "notification_type",
            "title",
            "message",
            "order_number",
            "is_read",
            "created_at",
        ]
        read_only_fields = fields

class AdminNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminNotification
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )        
