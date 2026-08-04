"""Keeps Product.average_rating / review_count in sync with approved
reviews — recomputed on every relevant change rather than incrementally
adjusted, to stay correct even after admin approve/unapprove toggles or
manual edits in Django Admin."""

from decimal import ROUND_HALF_UP, Decimal

from django.db.models import Avg, Count
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.products.models import Product

from .models import Review


def _recalculate(product_id):
    stats = Review.objects.filter(product_id=product_id, is_approved=True).aggregate(
        avg=Avg("rating"), count=Count("id")
    )
    avg_rating = stats["avg"] or 0
    Product.objects.filter(pk=product_id).update(
        average_rating=Decimal(str(avg_rating)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        ),
        review_count=stats["count"],
    )


@receiver(post_save, sender=Review)
def review_saved(sender, instance, **kwargs):
    _recalculate(instance.product_id)


@receiver(post_delete, sender=Review)
def review_deleted(sender, instance, **kwargs):
    _recalculate(instance.product_id)
