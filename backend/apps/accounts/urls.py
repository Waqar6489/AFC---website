from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AddressViewSet, ProfileView, WishlistViewSet

router = DefaultRouter()
router.register("addresses", AddressViewSet, basename="address")
router.register("wishlist", WishlistViewSet, basename="wishlist")

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("", include(router.urls)),
]
