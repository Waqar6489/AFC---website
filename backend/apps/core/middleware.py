import logging
import time

logger = logging.getLogger("apps")


class RequestLoggingMiddleware:
    """Lightweight request/response logger — logs method, path, status
    code and duration for every request. Useful for debugging and audit
    trails without the overhead of a full APM agent."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.monotonic()
        response = self.get_response(request)
        duration_ms = (time.monotonic() - start) * 1000

        if not request.path.startswith("/static/") and not request.path.startswith(
            "/media/"
        ):
            logger.info(
                "%s %s -> %s (%.1fms)",
                request.method,
                request.get_full_path(),
                response.status_code,
                duration_ms,
            )
        return response
