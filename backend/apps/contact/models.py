from django.db import models

from apps.accounts.models import User
from apps.core.models import TimeStampedModel
from apps.core.validators import validate_phone_number


class ContactMessage(TimeStampedModel):
    """A message submitted through the Contact Us form. Admin can reply
    and mark resolved, per spec."""

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(
        max_length=20, blank=True, validators=[validate_phone_number]
    )
    subject = models.CharField(max_length=200)
    message = models.TextField()

    is_resolved = models.BooleanField(default=False)
    admin_reply = models.TextField(blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    replied_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject} — {self.name}"


class NewsletterSubscriber(TimeStampedModel):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email
