"""Development settings — never use in production."""

from .base import *  # noqa: F401,F403

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Use local filesystem storage in dev unless Cloudinary creds are provided,
# so the project runs immediately after `pip install` without any external
# service configured.
if not env("CLOUDINARY_CLOUD_NAME", default=""):
    STORAGES = {  # noqa: F405
        **STORAGES,  # noqa: F405
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    }

# Dev machines often don't have Redis running locally. Fall back to
# Django's local-memory cache automatically unless a real REDIS_URL is
# configured, so `pip install -r requirements.txt && python manage.py
# runserver` works immediately with zero extra services running.
_redis_url = env("REDIS_URL", default="")
if not _redis_url or _redis_url == "redis://localhost:6379/0":
    try:
        import redis as _redis_client

        _redis_client.Redis.from_url(_redis_url or "redis://localhost:6379/0").ping()
        _redis_available = True
    except Exception:
        _redis_available = False

    if not _redis_available:
        CACHES = {
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                "LOCATION": "afc-dev-cache",
            }
        }

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
