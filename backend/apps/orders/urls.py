from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CartItemViewSet,
    CartView,
    CheckoutView,
    DeliveryEligibilityView,
    OrderViewSet,
)

router = DefaultRouter()
router.register("cart-items", CartItemViewSet, basename="cart-item")
router.register("history", OrderViewSet, basename="order")

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path("check-delivery/", DeliveryEligibilityView.as_view(), name="check-delivery"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("", include(router.urls)),
]
