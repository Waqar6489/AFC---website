from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from cloudinary.models import CloudinaryField
from apps.categories.models import Category
from apps.core.models import TimeStampedModel
from apps.core.utils import generate_unique_slug


class Addon(TimeStampedModel):
    """Global extra add-on customers can attach to a product at checkout
    (cheese, sauce, drinks, desserts, per spec)."""

    class AddonCategory(models.TextChoices):
        CHEESE = "cheese", "Cheese"
        SAUCE = "sauce", "Sauce"
        DRINKS = "drinks", "Drinks"
        DESSERTS = "desserts", "Desserts"

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=AddonCategory.choices)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal("0"))]
    )
    image = CloudinaryField("image", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Product(TimeStampedModel):
    """Core catalog item. Base `price`/`stock` are used directly for
    products with no size variants; when variants exist, each variant
    carries its own price and stock (see ProductVariant)."""

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=230, unique=True, blank=True)
    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    ingredients = models.TextField(
        blank=True, help_text="Comma-separated or free text list of ingredients."
    )

    # Nutrition facts — stored as discrete fields (rather than a loose
    # JSON blob) so they can be filtered/validated and rendered in a
    # consistent nutrition-facts table on the frontend.
    calories = models.PositiveIntegerField(null=True, blank=True)
    protein_g = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    carbs_g = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    fat_g = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    sugar_g = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    sku = models.CharField(max_length=64, unique=True)
    barcode = models.CharField(max_length=64, unique=True, blank=True, null=True)

    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0"))]
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0"))],
    )

    stock = models.PositiveIntegerField(default=0)
    track_inventory = models.BooleanField(default=True)

    available_addons = models.ManyToManyField(
        Addon, blank=True, related_name="products"
    )
    related_products = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=True,
        help_text=(
            "Manually curated related products. If left empty, the frontend "
            "falls back to same-category products."
        ),
    )
    frequently_bought_with = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=True,
    )

    is_active = models.BooleanField(default=True)
    is_trending = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)

    # Denormalized rating fields, kept in sync by a signal in apps.reviews
    # whenever a review is approved/unapproved/deleted — avoids an
    # aggregate query on every product list request.
    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=Decimal("0.00")
    )
    review_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_active", "category"]),
            models.Index(fields=["is_trending"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["is_best_seller"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Product, self.name, instance=self)
        super().save(*args, **kwargs)

    @property
    def effective_price(self):
        return self.discount_price if self.discount_price else self.price

    @property
    def discount_percentage(self):
        if self.discount_price and self.price:
            return round((1 - (self.discount_price / self.price)) * 100)
        return 0

    @property
    def in_stock(self):
        if not self.track_inventory:
            return True
        if self.variants.exists():
            return self.variants.filter(stock__gt=0).exists()
        return self.stock > 0


class ProductVariant(TimeStampedModel):
    """A size option for a product, each with its own price and stock —
    per spec: Small / Medium / Large / Extra Large, each priced
    independently."""

    class Size(models.TextChoices):
        SMALL = "small", "Small"
        MEDIUM = "medium", "Medium"
        LARGE = "large", "Large"
        EXTRA_LARGE = "extra_large", "Extra Large"
        ONE_POUND = "1_pound", "1 Pound"
        TWO_POUNDS = "2_pounds", "2 Pounds"
        THREE_POUNDS = "3_pounds", "3 Pounds"
        FOUR_POUNDS = "4_pounds", "4 Pounds"
        FIVE_POUNDS = "5_pounds", "5 Pounds"

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    size = models.CharField(max_length=15, choices=Size.choices)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0"))]
    )
    stock = models.PositiveIntegerField(default=0)
    sku_suffix = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ["price"]
        unique_together = ("product", "size")

    def __str__(self):
        return f"{self.product.name} — {self.get_size_display()}"


class ProductImage(TimeStampedModel):
    """Gallery image for a product's detail page."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = CloudinaryField("image", blank=True, null=True)
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-is_primary"]

    def __str__(self):
        return f"Image for {self.product.name}"

    def save(self, *args, **kwargs):
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).exclude(
                pk=self.pk
            ).update(is_primary=False)
        super().save(*args, **kwargs)
