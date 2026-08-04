"""AFC - Ahmad Foods | Root URL configuration."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

api_v1_patterns = [
    path("auth/", include("apps.authentication.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("core/", include("apps.core.urls")),
    path("categories/", include("apps.categories.urls")),
    path("products/", include("apps.products.urls")),
    path("deals/", include("apps.deals.urls")),
    path("orders/", include("apps.orders.urls")),
    path("reviews/", include("apps.reviews.urls")),
    path("faq/", include("apps.faq.urls")),
    path("team/", include("apps.team.urls")),
    path("contact/", include("apps.contact.urls")),
    path("notifications/", include("apps.notifications.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(api_v1_patterns)),
    # API documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "AFC - Ahmad Foods Administration"
admin.site.site_title = "AFC Admin Portal"
admin.site.index_title = "Sweets & Bakers — Management Dashboard"
