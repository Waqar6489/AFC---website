from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.permissions import IsAdminRole
from apps.core.utils import send_templated_email
from apps.notifications.models import AdminNotification
from .models import ContactMessage
from .serializers import (
    ContactMessageAdminSerializer,
    ContactMessageCreateSerializer,
    NewsletterSubscribeSerializer,
)


class ContactMessageCreateView(generics.CreateAPIView):
    """Public Contact Us form submission."""

    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageCreateSerializer
    permission_classes = [permissions.AllowAny]
    throttle_scope = "contact_form"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        AdminNotification.objects.create(
        notification_type=AdminNotification.NotificationType.CONTACT,
        title="New Contact Message",
        message=f"{message.name} sent a new message."
)

        send_templated_email(
            subject="We received your message — AFC - Ahmad Foods",
            template_name="emails/contact_received.html",
            context={"name": message.name, "subject": message.subject},
            to_email=message.email,
        )

        return Response(
            {
                "success": True,
                "message": "Your message has been received. We'll get back to you soon.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class ContactMessageAdminViewSet(viewsets.ModelViewSet):
    """Admin-only inbox: view all messages, reply, mark resolved."""

    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]
    filterset_fields = ["is_resolved"]
    http_method_names = ["get", "patch", "delete", "head", "options"]


class NewsletterSubscribeView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "contact_form"

    def post(self, request):
        serializer = NewsletterSubscribeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": True,
                "message": "Thanks for subscribing to our newsletter!",
                "errors": {},
            },
            status=status.HTTP_201_CREATED,
        )
