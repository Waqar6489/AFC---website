"""Settings used exclusively by the automated test suite (pytest).

Identical to dev.py except: throttling is disabled so a large test suite
hammering /auth/login/ repeatedly doesn't trip rate limits that exist to
protect production from brute-force attacks — that's tested separately
in TestThrottling below, in isolation, with an explicit low rate.
"""

from .dev import *  # noqa: F401,F403

REST_FRAMEWORK = {
    **REST_FRAMEWORK,  # noqa: F405
    "DEFAULT_THROTTLE_CLASSES": [],
    "DEFAULT_THROTTLE_RATES": {},
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher"
]  # fast hashing in tests only
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
