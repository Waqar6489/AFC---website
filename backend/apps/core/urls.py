from django.urls import path

from .views import AdminAnalyticsView, SiteConfigView

urlpatterns = [
    path("site-config/", SiteConfigView.as_view(), name="site-config"),
    path("admin/analytics/", AdminAnalyticsView.as_view(), name="admin-analytics"),
]
