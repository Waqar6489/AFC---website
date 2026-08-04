from django.contrib import admin

from .models import SiteConfiguration


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    """Singleton admin — always edits the one SiteConfiguration row.
    This is where the restaurant's location for the delivery-radius
    feature is configured, per the project spec."""

    fieldsets = (
        ("Branding", {"fields": ("site_name", "tagline", "logo", "favicon")}),
        (
            "Delivery Radius (Haversine)",
            {
                "fields": (
                    "restaurant_latitude",
                    "restaurant_longitude",
                    "delivery_radius_km",
                ),
                "description": "Customers outside this radius from the restaurant cannot check out.",
            },
        ),
        (
            "Contact Info",
            {
                "fields": (
                    "contact_phone",
                    "contact_email",
                    "contact_address",
                    "working_hours",
                )
            },
        ),
        (
            "Social Links",
            {
                "fields": (
                    "facebook_url",
                    "instagram_url",
                    "twitter_url",
                    "whatsapp_number",
                )
            },
        ),
        ("System", {"fields": ("maintenance_mode",)}),
    )

    def has_add_permission(self, request):
        return not SiteConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SiteConfiguration.load()
        from django.shortcuts import redirect
        from django.urls import reverse

        return redirect(reverse("admin:core_siteconfiguration_change", args=[obj.pk]))
