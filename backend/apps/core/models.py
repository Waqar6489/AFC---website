from django.core.exceptions import ValidationError
from django.db import models
from cloudinary.models import CloudinaryField

class TimeStampedModel(models.Model):
    """Abstract base providing created_at / updated_at on every model in
    the project. All app models should inherit from this."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class SiteConfiguration(models.Model):
    """Singleton model editable from Django Admin that drives site-wide,
    non-hardcoded business settings — most importantly the restaurant's
    physical location used for the delivery-radius calculation."""

    site_name = models.CharField(max_length=150, default="AFC - Ahmad Foods")
    tagline = models.CharField(max_length=150, default="Sweets & Bakers")

    restaurant_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    restaurant_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    delivery_radius_km = models.DecimalField(
        max_digits=5, decimal_places=2, default=10.00
    )

    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_address = models.CharField(max_length=255, blank=True)
    working_hours = models.CharField(
        max_length=255, blank=True, help_text="e.g. Mon-Sun: 9:00 AM - 11:00 PM"
    )

    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)

    logo = CloudinaryField("logo", blank=True, null=True)
    favicon = CloudinaryField("favicon", blank=True, null=True)

    maintenance_mode = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # singleton — prevent accidental deletion

    def clean(self):
        if not (-90 <= float(self.restaurant_latitude) <= 90):
            raise ValidationError(
                {"restaurant_latitude": "Latitude must be between -90 and 90."}
            )
        if not (-180 <= float(self.restaurant_longitude) <= 180):
            raise ValidationError(
                {"restaurant_longitude": "Longitude must be between -180 and 180."}
            )

    @classmethod
    def load(cls):
        obj, _created = cls.objects.get_or_create(
            pk=1,
            defaults={
                "restaurant_latitude": 33.6844,
                "restaurant_longitude": 73.0479,
                "delivery_radius_km": 10.00,
            },
        )
        return obj
