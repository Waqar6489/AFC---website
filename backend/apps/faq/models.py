from django.db import models

from apps.core.models import TimeStampedModel


class FAQ(TimeStampedModel):
    """Frequently asked question, fully admin-managed per spec — ordering
    and a visibility toggle, shown on the homepage FAQ section."""

    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(
        default=0, help_text="Lower numbers display first."
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question
