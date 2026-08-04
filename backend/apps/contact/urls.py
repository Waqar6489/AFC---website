from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ContactMessageAdminViewSet,
    ContactMessageCreateView,
    NewsletterSubscribeView,
)

router = DefaultRouter()
router.register(
    "messages", ContactMessageAdminViewSet, basename="contact-message-admin"
)

urlpatterns = [
    path("submit/", ContactMessageCreateView.as_view(), name="contact-submit"),
    path(
        "newsletter/subscribe/",
        NewsletterSubscribeView.as_view(),
        name="newsletter-subscribe",
    ),
    path("", include(router.urls)),
]
