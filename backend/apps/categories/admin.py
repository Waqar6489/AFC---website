from django.contrib import admin
from django.utils.html import format_html

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "thumbnail",
        "name",
        "order",
        "is_active",
        "product_count",
        "created_at",
    )
    list_editable = ("order",)
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order", "name")

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:4px;" />',
                obj.image.url,
            )
        return "—"

    thumbnail.short_description = "Image"

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = "Products"
