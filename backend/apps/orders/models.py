import random
import string
from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from apps.accounts.models import Address, User
from apps.core.models import TimeStampedModel
from apps.products.models import Addon, Product, ProductVariant


def _generate_order_number():
    date_part = timezone.now().strftime("%Y%m%d")
    random_part = "".join(random.choices(string.digits, k=5))
    return f"AFC-{date_part}-{random_part}"


class Cart(TimeStampedModel):
    """One persistent cart per authenticated user — per spec, only logged
    in users can add to cart, so there is no anonymous/session cart."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")

    def __str__(self):
        return f"Cart for {self.user.email}"

    @property
    def subtotal(self):
        return sum((item.line_total for item in self.items.all()), Decimal("0.00"))

    @property
    def item_count(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(TimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, null=True, blank=True
    )
    addons = models.ManyToManyField(Addon, blank=True)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def unit_price(self):
        base = self.variant.price if self.variant else self.product.effective_price
        addons_total = sum(
            (addon.price for addon in self.addons.all()), Decimal("0.00")
        )
        return base + addons_total

    @property
    def line_total(self):
        return self.unit_price * self.quantity


class Order(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        PREPARING = "preparing", "Preparing"
        COOKING = "cooking", "Cooking"
        PACKING = "packing", "Packing"
        READY_FOR_PICKUP = "ready_for_pickup", "Ready For Pickup"
        OUT_FOR_DELIVERY = "out_for_delivery", "Out For Delivery"
        NEARBY = "nearby", "Nearby"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"
        REFUNDED = "refunded", "Refunded"

    class PaymentMethod(models.TextChoices):
        COD = "cod", "Cash On Delivery"
        STRIPE = "stripe", "Card (Stripe)"

    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"

    order_number = models.CharField(max_length=30, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders")

    # Delivery address is snapshotted at order time (not just FK'd) so
    # historical orders remain accurate even if the customer later edits
    # or deletes the saved address.
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders"
    )
    delivery_full_name = models.CharField(max_length=150)
    delivery_phone = models.CharField(max_length=20)
    delivery_address_line = models.CharField(max_length=255)
    delivery_city = models.CharField(max_length=100)
    delivery_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    delivery_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    distance_km = models.DecimalField(max_digits=6, decimal_places=2)

    notes = models.CharField(max_length=500, blank=True)

    coupon_code = models.CharField(max_length=40, blank=True, null=True)
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"),)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(
        max_length=10, choices=PaymentMethod.choices, default=PaymentMethod.COD
    )
    payment_status = models.CharField(
        max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["order_number"]),
        ]

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = _generate_order_number()
            while Order.objects.filter(order_number=self.order_number).exists():
                self.order_number = _generate_order_number()
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name="order_items"
    )

    # Snapshots — an order must remain historically accurate even if the
    # product is later renamed, repriced, or deleted.
    product_name = models.CharField(max_length=200)
    variant_size = models.CharField(max_length=20, blank=True)
    addons_snapshot = models.JSONField(default=list, blank=True)

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"


class OrderStatusHistory(models.Model):
    """Backs the professional order-tracking timeline UI."""

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="status_history"
    )
    status = models.CharField(max_length=20, choices=Order.Status.choices)
    note = models.CharField(max_length=255, blank=True)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["changed_at"]
        verbose_name_plural = "Order status histories"

    def __str__(self):
        return f"{self.order.order_number} → {self.status}"
