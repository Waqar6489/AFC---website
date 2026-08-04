from django.contrib import admin

from apps.core.admin_mixins import CSVExportMixin

from .models import Review


@admin.register(Review)
class ReviewAdmin(CSVExportMixin, admin.ModelAdmin):
    list_display = (
        "product",
        "user",
        "rating",
        "is_verified_purchase",
        "is_approved",
        "created_at",
    )
    list_filter = ("is_approved", "is_verified_purchase", "rating")
    search_fields = ("product__name", "user__email", "comment")
    autocomplete_fields = ("product", "user", "order")
    actions = ["approve_reviews", "unapprove_reviews", "export_as_csv"]
    csv_export_fields = ["id", "product", "user", "rating", "is_approved", "created_at"]

    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        for review in queryset:
            review.save()  # ensures the post_save signal recalculates product aggregates
        self.message_user(request, f"{updated} review(s) approved.")

    approve_reviews.short_description = "Approve selected reviews"

    def unapprove_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        for review in queryset:
            review.save()
        self.message_user(request, f"{updated} review(s) unapproved.")

    unapprove_reviews.short_description = "Unapprove selected reviews"
