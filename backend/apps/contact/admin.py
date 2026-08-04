from django.contrib import admin
from django.utils import timezone

from apps.core.admin_mixins import CSVExportMixin

from .models import ContactMessage, NewsletterSubscriber


@admin.register(ContactMessage)
class ContactMessageAdmin(CSVExportMixin, admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_resolved", "created_at")
    list_filter = ("is_resolved", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "phone", "subject", "message", "created_at")
    actions = ["mark_resolved", "export_as_csv"]
    csv_export_fields = ["id", "name", "email", "subject", "is_resolved", "created_at"]

    fieldsets = (
        (
            "Submitted Message",
            {"fields": ("name", "email", "phone", "subject", "message", "created_at")},
        ),
        (
            "Admin Response",
            {"fields": ("admin_reply", "is_resolved", "replied_by", "replied_at")},
        ),
    )

    def save_model(self, request, obj, form, change):
        if obj.admin_reply and not obj.replied_at:
            obj.replied_at = timezone.now()
            obj.replied_by = request.user
        super().save_model(request, obj, form, change)

    def mark_resolved(self, request, queryset):
        updated = queryset.update(is_resolved=True)
        self.message_user(request, f"{updated} message(s) marked resolved.")

    mark_resolved.short_description = "Mark selected as resolved"


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(CSVExportMixin, admin.ModelAdmin):
    list_display = ("email", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("email",)
    csv_export_fields = ["email", "is_active", "created_at"]
