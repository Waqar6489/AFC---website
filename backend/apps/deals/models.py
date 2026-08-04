from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField
from apps.categories.models import Category
from apps.core.models import TimeStampedModel
from apps.core.utils import generate_unique_slug
from apps.products.models import Product


class Deal(TimeStampedModel):
    """A promotional deal — an offer banner with a countdown timer, an
    automatic product/category discount, and/or a coupon code, per spec.
    Fully managed from Django Admin."""

    class DiscountType(models.TextChoices):
        PERCENTAGE = "percentage", "Percentage"
        FIXED = "fixed", "Fixed Amount"

    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        ACTIVE = "active", "Active"
        EXPIRED = "expired", "Expired"
        DISABLED = "disabled", "Disabled"

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    description = models.TextField(blank=True)
    banner_image = CloudinaryField("banner_image", blank=True, null=True)

    discount_type = models.CharField(
        max_length=10, choices=DiscountType.choices, default=DiscountType.PERCENTAGE
    )
    discount_value = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal("0"))]
    )
    max_discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Optional cap on the discount amount for percentage-based deals.",
    )
    min_order_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0")
    )

    coupon_code = models.CharField(
        max_length=40,
        unique=True,
        blank=True,
        null=True,
        help_text=(
            "Leave blank for a deal that applies automatically to the linked "
            "products/categories without a code."
        ),
    )

    products = models.ManyToManyField(Product, blank=True, related_name="deals")
    categories = models.ManyToManyField(Category, blank=True, related_name="deals")

    usage_limit = models.PositiveIntegerField(
        null=True, blank=True, help_text="Leave blank for unlimited total uses."
    )
    used_count = models.PositiveIntegerField(default=0)
    per_user_limit = models.PositiveIntegerField(default=1)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Deal, self.title, instance=self)
        super().save(*args, **kwargs)

    @property
    def status(self):
        if not self.is_active:
            return self.Status.DISABLED
        now = timezone.now()
        if now < self.start_date:
            return self.Status.SCHEDULED
        if now > self.end_date:
            return self.Status.EXPIRED
        if self.usage_limit and self.used_count >= self.usage_limit:
            return self.Status.EXPIRED
        return self.Status.ACTIVE

    @property
    def is_currently_active(self):
        return self.status == self.Status.ACTIVE

    def calculate_discount(self, order_amount: Decimal) -> Decimal:
        """Returns the discount amount (never more than order_amount) for
        a given cart/order subtotal."""
        if self.discount_type == self.DiscountType.PERCENTAGE:
            discount = (self.discount_value / Decimal("100")) * order_amount
            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)
        else:
            discount = self.discount_value
        return min(discount, order_amount)
