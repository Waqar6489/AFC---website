"""Shared, cross-app utility functions."""

import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger("apps")


def send_templated_email(
    subject: str, template_name: str, context: dict, to_email: str
) -> bool:
    """Renders an HTML email template (with an auto-generated plaintext
    fallback) and sends it. Returns True on success, False otherwise —
    callers should not let email failures break the request/response
    cycle (e.g. registration must still succeed even if SMTP is down)."""
    try:
        html_body = render_to_string(template_name, context)
        text_body = strip_tags(html_body)
        message = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        message.attach_alternative(html_body, "text/html")
        message.send(fail_silently=False)
        return True
    except Exception:  # noqa: BLE001 — email delivery must never crash the request
        logger.exception("Failed to send email '%s' to %s", subject, to_email)
        return False


def generate_unique_slug(
    model_class, value: str, slug_field: str = "slug", instance=None
) -> str:
    """Generates a unique slug for `value`, appending -2, -3, ... on
    collision. Excludes `instance` itself when updating an existing row."""
    from django.utils.text import slugify

    base_slug = slugify(value)[:200] or "item"
    slug = base_slug
    counter = 2
    queryset = model_class.objects.all()
    if instance and instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    while queryset.filter(**{slug_field: slug}).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug
