from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action,api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import Notification,AdminNotification
from .serializers import NotificationSerializer, AdminNotificationSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """User-scoped notification inbox: list, retrieve, mark one/all as
    read. Notifications themselves are created server-side by signals
    (order status changes) — there is no create endpoint."""

    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["is_read", "notification_type"]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=True, methods=["post"], url_path="mark-read")
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save(update_fields=["is_read"])
        return Response(
            {"success": True, "message": "Notification marked as read."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"], url_path="mark-all-read")
    def mark_all_read(self, request):
        updated = self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response(
            {"success": True, "message": f"{updated} notification(s) marked as read."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"], url_path="unread-count")
    def unread_count(self, request):
        count = self.get_queryset().filter(is_read=False).count()
        return Response(
            {"success": True, "data": {"unread_count": count}},
            status=status.HTTP_200_OK,
        )


class AdminNotificationViewSet(viewsets.ModelViewSet):
    serializer_class = AdminNotificationSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return AdminNotification.objects.all().order_by("-created_at")

    @action(detail=False, methods=["get"], url_path="unread-count")
    def unread_count(self, request):
       count = self.get_queryset().filter(is_read=False).count()
       return Response({
               "success": True,
               "data": {
                   "count": count
               }
           })
    

    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save(update_fields=["is_read"])

        return Response({
            "success": True,
            "message": "Notification marked as read."
        })

    @action(detail=False, methods=["post"])
    def mark_all_read(self, request):
        updated = AdminNotification.objects.filter(is_read=False).update(is_read=True)

        return Response({
            "success": True,
            "message": f"{updated} notifications marked as read."
        })

