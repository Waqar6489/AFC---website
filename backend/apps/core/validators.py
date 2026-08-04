"""Shared validators."""

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class PasswordComplexityValidator:
    """Requires at least one uppercase letter, one lowercase letter, one
    digit, and one special character — on top of Django's built-in
    validators (min length, not too common, not fully numeric)."""

    def validate(self, password, user=None):
        if not re.search(r"[A-Z]", password):
            raise ValidationError(
                _("Password must contain at least one uppercase letter."),
                code="password_no_upper",
            )
        if not re.search(r"[a-z]", password):
            raise ValidationError(
                _("Password must contain at least one lowercase letter."),
                code="password_no_lower",
            )
        if not re.search(r"\d", password):
            raise ValidationError(
                _("Password must contain at least one digit."),
                code="password_no_digit",
            )
        if not re.search(r"[^A-Za-z0-9]", password):
            raise ValidationError(
                _("Password must contain at least one special character."),
                code="password_no_special",
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 8 characters, including "
            "one uppercase letter, one lowercase letter, one digit, and "
            "one special character."
        )


def validate_phone_number(value):
    pattern = r"^\+?[0-9]{10,15}$"
    if not re.match(pattern, value):
        raise ValidationError(
            _("Enter a valid phone number (10-15 digits, optional leading +).")
        )
