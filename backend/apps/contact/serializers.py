from django.utils import timezone
from rest_framework import serializers

from .models import ContactMessage, NewsletterSubscriber


class ContactMessageCreateSerializer(serializers.ModelSerializer):
    """Public-facing serializer used by the Contact Us form."""

    class Meta:
        model = ContactMessage
        fields = ["id", "name", "email", "phone", "subject", "message", "created_at"]
        read_only_fields = ["id", "created_at"]


class ContactMessageAdminSerializer(serializers.ModelSerializer):
    """Used by admin/staff to view + reply to a message."""

    class Meta:
        model = ContactMessage
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "subject",
            "message",
            "is_resolved",
            "admin_reply",
            "replied_at",
            "replied_by",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "name",
            "email",
            "phone",
            "subject",
            "message",
            "replied_at",
            "replied_by",
            "created_at",
        ]

    def update(self, instance, validated_data):
        request = self.context["request"]
        new_reply = validated_data.get("admin_reply")
        if new_reply and new_reply != instance.admin_reply:
            validated_data["replied_at"] = timezone.now()
            validated_data["replied_by"] = request.user
        return super().update(instance, validated_data)


class NewsletterSubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ["id", "email", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_email(self, value):
        value = value.lower().strip()
        existing = NewsletterSubscriber.objects.filter(email__iexact=value).first()
        if existing and existing.is_active:
            raise serializers.ValidationError("This email is already subscribed.")
        return value

    def create(self, validated_data):
        subscriber, _created = NewsletterSubscriber.objects.update_or_create(
            email=validated_data["email"], defaults={"is_active": True}
        )
        return subscriber
