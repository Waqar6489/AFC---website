
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    NotificationViewSet,
    AdminNotificationViewSet
)

router = DefaultRouter()
router.register("", NotificationViewSet, basename="notification")
router.register(
    "admin-notifications",
    AdminNotificationViewSet,
    basename="admin-notifications",
)


urlpatterns = router.urls