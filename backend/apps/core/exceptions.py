"""Custom DRF exception handler producing a consistent error envelope:

{
    "success": false,
    "message": "<human readable summary>",
    "errors": { ... field level errors ... }
}
"""

import logging

from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions as drf_exceptions
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger("apps")


def custom_exception_handler(exc, context):
    if isinstance(exc, Http404):
        exc = drf_exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = drf_exceptions.PermissionDenied()

    response = drf_exception_handler(exc, context)

    if response is None:
        logger.exception("Unhandled exception: %s", exc)
        return Response(
            {
                "success": False,
                "message": "An unexpected error occurred. Please try again later.",
                "errors": {},
            },
            status=500,
        )

    if isinstance(response.data, dict) and "detail" in response.data:
        message = str(response.data["detail"])
        errors = {}
    elif isinstance(response.data, dict):
        message = "Validation failed. Please check the submitted data."
        errors = response.data
    elif isinstance(response.data, list):
        message = "Validation failed. Please check the submitted data."
        errors = {"non_field_errors": response.data}
    else:
        message = str(response.data)
        errors = {}

    response.data = {"success": False, "message": message, "errors": errors}
    return response


class BusinessLogicError(drf_exceptions.APIException):
    """Raised for domain-specific errors (e.g. delivery radius exceeded,
    coupon expired) that don't map cleanly to a standard DRF exception."""

    status_code = 400
    default_detail = "This action could not be completed."
    default_code = "business_logic_error"
