from rest_framework.routers import DefaultRouter

from .views import AddonViewSet, ProductViewSet

router = DefaultRouter()
router.register("addons", AddonViewSet, basename="addon")
router.register("", ProductViewSet, basename="product")

urlpatterns = router.urls
