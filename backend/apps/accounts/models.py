import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField
from apps.core.models import TimeStampedModel
from apps.core.validators import validate_phone_number

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom, email-based user. UUID primary key is used deliberately to
    prevent user-ID enumeration attacks on public-facing endpoints (e.g.
    order lookups, review authorship)."""

    class Role(models.TextChoices):
        CUSTOMER = "customer", _("Customer")
        STAFF = "staff", _("Staff")
        ADMIN = "admin", _("Admin")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(_("email address"), unique=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(
        max_length=20, blank=True, validators=[validate_phone_number]
    )
    avatar = CloudinaryField("avatar", blank=True, null=True)

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CUSTOMER)

    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    class Meta:
        ordering = ["-date_joined"]
        indexes = [models.Index(fields=["email"]), models.Index(fields=["role"])]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN or self.is_staff


class Address(TimeStampedModel):
    """A customer's saved delivery address. `latitude`/`longitude` are
    captured client-side (browser Geolocation API or map pin) and are
    what the backend uses to enforce the delivery radius at checkout."""

    class Label(models.TextChoices):
        HOME = "home", _("Home")
        WORK = "work", _("Work")
        OTHER = "other", _("Other")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    label = models.CharField(max_length=10, choices=Label.choices, default=Label.HOME)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, validators=[validate_phone_number])

    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default="Pakistan")

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ["-is_default", "-created_at"]
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.full_name} — {self.address_line}, {self.city}"

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(
                pk=self.pk
            ).update(is_default=False)
        super().save(*args, **kwargs)


class WishlistItem(TimeStampedModel):
    """A product a user has saved to their wishlist. Product is imported
    lazily by string reference to avoid a circular import (products app
    is loaded after accounts in INSTALLED_APPS)."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="wishlist_items"
    )
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="wishlisted_by"
    )

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.email} ♥ {self.product.name}"
