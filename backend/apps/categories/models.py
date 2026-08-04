from django.db import models

from apps.core.models import TimeStampedModel
from apps.core.utils import generate_unique_slug
from cloudinary.models import CloudinaryField

class Category(TimeStampedModel):
    """Product category, fully manageable from Django Admin per spec —
    image, ordering, and visibility toggle."""

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = CloudinaryField("Category_Image", blank=True, null=True)

    order = models.PositiveIntegerField(
        default=0, help_text="Lower numbers display first on the homepage."
    )
    is_active = models.BooleanField(
        default=True, help_text="Uncheck to hide this category everywhere on the site."
    )

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Categories"
        indexes = [models.Index(fields=["is_active", "order"])]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Category, self.name, instance=self)
        super().save(*args, **kwargs)
