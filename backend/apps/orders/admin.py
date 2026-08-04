from django.contrib import admin

from apps.core.admin_mixins import CSVExportMixin

from .models import Cart, CartItem, Order, OrderItem, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        "product",
        "product_name",
        "variant_size",
        "addons_snapshot",
        "unit_price",
        "quantity",
        "line_total",
    )
    can_delete = False


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ("status", "note", "changed_by", "changed_at")
    can_delete = False


@admin.register(Order)
class OrderAdmin(CSVExportMixin, admin.ModelAdmin):
    list_display = (
        "order_number",
        "user",
        "status",
        "payment_method",
        "payment_status",
        "total_amount",
        "distance_km",
        "created_at",
    )
    list_filter = ("status", "payment_method", "payment_status", "created_at")
    search_fields = ("order_number", "user__email", "delivery_phone")
    readonly_fields = (
        "order_number",
        "user",
        "address",
        "delivery_full_name",
        "delivery_phone",
        "delivery_address_line",
        "delivery_city",
        "delivery_latitude",
        "delivery_longitude",
        "distance_km",
        "subtotal",
        "discount_amount",
        "total_amount",
        "coupon_code",
        "created_at",
        "updated_at",
    )
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    autocomplete_fields = ["user"]
    csv_export_fields = [
        "order_number",
        "user",
        "status",
        "payment_status",
        "total_amount",
        "created_at",
    ]

    fieldsets = (
        ("Order", {"fields": ("order_number", "user", "status", "notes")}),
        (
            "Delivery",
            {
                "fields": (
                    "delivery_full_name",
                    "delivery_phone",
                    "delivery_address_line",
                    "delivery_city",
                    "delivery_latitude",
                    "delivery_longitude",
                    "distance_km",
                )
            },
        ),
        (
            "Payment",
            {
                "fields": (
                    "payment_method",
                    "payment_status",
                    "subtotal",
                    "discount_amount",
                    "coupon_code",
                    "total_amount",
                )
            },
        ),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def save_model(self, request, obj, form, change):
        if change:
            original = Order.objects.get(pk=obj.pk)
            if original.status != obj.status:
                OrderStatusHistory.objects.create(
                    order=obj,
                    status=obj.status,
                    changed_by=request.user,
                    note=f"Status changed via admin by {request.user.email}",
                )
        super().save_model(request, obj, form, change)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "item_count", "subtotal", "updated_at")
    search_fields = ("user__email",)


admin.site.register(CartItem)
