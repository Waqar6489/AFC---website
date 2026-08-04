from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from cloudinary.models import CloudinaryField
from apps.accounts.models import User
from apps.core.models import TimeStampedModel
from apps.orders.models import Order
from apps.products.models import Product


class Review(TimeStampedModel):
    """Only verified buyers (users with a Delivered order containing this
    product) may create a review — enforced in the serializer, not just
    the frontend. Reviews require admin approval before they're publicly
    visible, per spec."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True, related_name="reviews"
    )

    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    image = CloudinaryField("Review_Image", blank=True, null=True)

    is_verified_purchase = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("product", "user", "order")

    def __str__(self):
        return f"{self.rating}★ review of {self.product.name} by {self.user.email}"
