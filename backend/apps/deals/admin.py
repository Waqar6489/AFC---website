from django.contrib import admin

from apps.core.admin_mixins import CSVExportMixin

from .models import Deal


@admin.register(Deal)
class DealAdmin(CSVExportMixin, admin.ModelAdmin):
    list_display = (
        "title",
        "discount_type",
        "discount_value",
        "coupon_code",
        "start_date",
        "end_date",
        "status_badge",
        "used_count",
        "is_active",
    )
    list_filter = ("discount_type", "is_active")
    search_fields = ("title", "coupon_code")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("products", "categories")
    readonly_fields = ("used_count",)
    csv_export_fields = [
        "id",
        "title",
        "coupon_code",
        "discount_type",
        "discount_value",
        "start_date",
        "end_date",
        "used_count",
    ]

    fieldsets = (
        ("Basic Info", {"fields": ("title", "slug", "description", "banner_image")}),
        (
            "Discount",
            {
                "fields": (
                    "discount_type",
                    "discount_value",
                    "max_discount_amount",
                    "min_order_amount",
                )
            },
        ),
        (
            "Coupon",
            {"fields": ("coupon_code", "usage_limit", "used_count", "per_user_limit")},
        ),
        ("Scope", {"fields": ("products", "categories")}),
        ("Schedule & Status", {"fields": ("start_date", "end_date", "is_active")}),
    )

    def status_badge(self, obj):
        colors = {
            "active": "#16a34a",
            "scheduled": "#2563eb",
            "expired": "#dc2626",
            "disabled": "#6b7280",
        }
        from django.utils.html import format_html

        return format_html(
            '<span style="color:{};font-weight:600;">{}</span>',
            colors.get(obj.status, "#000"),
            obj.status.upper(),
        )

    status_badge.short_description = "Status"
