from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """Generates a single-use token for email verification links. Including
    `is_email_verified` in the hash means the token automatically becomes
    invalid the moment the address is verified — it can't be replayed."""

    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_email_verified}{user.email}"


email_verification_token = EmailVerificationTokenGenerator()
