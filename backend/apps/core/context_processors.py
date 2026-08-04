from apps.notifications.models import AdminNotification


def admin_notifications(request):
    if request.user.is_authenticated and request.user.is_staff:
        unread_count = AdminNotification.objects.filter(
            is_read=False
        ).count()

        latest_notifications = AdminNotification.objects.filter(
            is_read=False
        ).order_by("-created_at")[:5]

        return {
            "admin_unread_notifications": unread_count,
            "admin_notifications": latest_notifications,
        }

    return {
        "admin_unread_notifications": 0,
        "admin_notifications": [],
    }