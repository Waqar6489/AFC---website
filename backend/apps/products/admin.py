from django.contrib import admin
from django.utils.html import format_html

from apps.core.admin_mixins import CSVExportMixin

from .models import Addon, Product, ProductImage, ProductVariant


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(CSVExportMixin, admin.ModelAdmin):
    list_display = (
        "thumbnail",
        "name",
        "category",
        "price",
        "discount_price",
        "stock",
        "is_active",
        "is_trending",
        "is_featured",
        "is_best_seller",
        "average_rating",
    )
    list_editable = (
        "price",
        "discount_price",
        "stock",
        "is_active",
        "is_trending",
        "is_featured",
        "is_best_seller",
    )
    list_filter = (
        "category",
        "is_active",
        "is_trending",
        "is_featured",
        "is_best_seller",
    )
    search_fields = ("name", "sku", "barcode", "description")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("category",)
    filter_horizontal = (
        "available_addons",
        "related_products",
        "frequently_bought_with",
    )
    readonly_fields = ("average_rating", "review_count")
    inlines = [ProductVariantInline, ProductImageInline]
    csv_export_fields = [
        "id",
        "name",
        "sku",
        "category",
        "price",
        "discount_price",
        "stock",
        "is_active",
    ]

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "category",
                    "name",
                    "slug",
                    "short_description",
                    "description",
                )
            },
        ),
        (
            "Details",
            {
                "fields": (
                    "ingredients",
                    "calories",
                    "protein_g",
                    "carbs_g",
                    "fat_g",
                    "sugar_g",
                )
            },
        ),
        (
            "Inventory",
            {
                "fields": (
                    "sku",
                    "barcode",
                    "price",
                    "discount_price",
                    "stock",
                    "track_inventory",
                )
            },
        ),
        (
            "Merchandising",
            {"fields": ("is_active", "is_trending", "is_featured", "is_best_seller")},
        ),
        (
            "Cross-sell",
            {
                "fields": (
                    "available_addons",
                    "related_products",
                    "frequently_bought_with",
                )
            },
        ),
        (
            "Ratings (read-only, updated automatically)",
            {"fields": ("average_rating", "review_count")},
        ),
    )

    def thumbnail(self, obj):
        primary = obj.images.filter(is_primary=True).first() or obj.images.first()
        if primary:
            return format_html(
                '<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:4px;" />',
                primary.image.url,
            )
        return "—"

    thumbnail.short_description = "Image"


@admin.register(Addon)
class AddonAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name",)
