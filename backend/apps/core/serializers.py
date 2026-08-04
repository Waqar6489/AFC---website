from rest_framework import serializers

from .models import SiteConfiguration


class PublicSiteConfigSerializer(serializers.ModelSerializer):
    """Publicly-readable subset of SiteConfiguration — used by the
    frontend footer, Contact Us page, and Google Map embed. Deliberately
    excludes internal-only fields like `maintenance_mode`."""
    favicon = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()
    class Meta:
        model = SiteConfiguration
        fields = [
            "site_name",
            "tagline",
            "logo",
            "favicon",
            "restaurant_latitude",
            "restaurant_longitude",
            "delivery_radius_km",
            "contact_phone",
            "contact_email",
            "contact_address",
            "working_hours",
            "facebook_url",
            "instagram_url",
            "twitter_url",
            "whatsapp_number",
        ]
    def get_favicon(self, obj):
        if obj.favicon:
            return obj.favicon.url
        return None
    def get_logo(self, obj):
        if obj.logo:
            return obj.logo.url
        return None
