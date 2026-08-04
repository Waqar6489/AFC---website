from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DealViewSet, ValidateCouponView

router = DefaultRouter()
router.register("", DealViewSet, basename="deal")

urlpatterns = [
    path("validate-coupon/", ValidateCouponView.as_view(), name="validate-coupon"),
    path("", include(router.urls)),
]
