"""Admin dashboard analytics — powers the 'Dashboard Analytics' section
of the admin panel described in the spec (revenue, customers, products,
orders, reviews, etc.) via a single aggregated endpoint. Django Admin
itself remains the primary CRUD/management interface; this endpoint is
for a summary dashboard view."""

from datetime import timedelta
from datetime import timezone as dt_timezone

from django.db.models import Count, Sum
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SiteConfiguration
from .permissions import IsAdminRole
from .serializers import PublicSiteConfigSerializer


class SiteConfigView(APIView):
    """Public read-only site info — contact details, social links,
    working hours, logo, and delivery radius. Used by the footer, Contact
    Us page, and the Google Map embed."""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        config = SiteConfiguration.load()
        serializer = PublicSiteConfigSerializer(config, context={"request": request})
        return Response(
            {"success": True, "message": "", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class AdminAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]

    def get(self, request):
        from apps.accounts.models import User
        from apps.categories.models import Category
        from apps.contact.models import ContactMessage
        from apps.deals.models import Deal
        from apps.orders.models import Order
        from apps.products.models import Product
        from apps.reviews.models import Review

        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=today_start.weekday())
        month_start = today_start.replace(day=1)

        paid_orders = Order.objects.exclude(
            status__in=[Order.Status.CANCELLED, Order.Status.PENDING]
        )

        def revenue_since(start):
            return (
                paid_orders.filter(created_at__gte=start).aggregate(
                    total=Sum("total_amount")
                )["total"]
                or 0
            )

        orders_by_status = dict(
            Order.objects.values_list("status").annotate(count=Count("id")).order_by()
        )

        top_products = (
            Product.objects.annotate(units_sold=Sum("order_items__quantity"))
            .filter(units_sold__gt=0)
            .order_by("-units_sold")[:5]
            .values("id", "name", "units_sold")
        )

        recent_orders = list(
            Order.objects.order_by("-created_at")[:10].values(
                "order_number", "user__email", "status", "total_amount", "created_at"
            )
        )

        data = {
            "revenue": {
                "today": revenue_since(today_start),
                "this_week": revenue_since(week_start),
                "this_month": revenue_since(month_start),
                "all_time": revenue_since(
                    timezone.datetime.min.replace(tzinfo=dt_timezone.utc)
                ),
            },
            "orders": {
                "total": Order.objects.count(),
                "by_status": orders_by_status,
                "recent": recent_orders,
            },
            "customers": {
                "total": User.objects.filter(role=User.Role.CUSTOMER).count(),
                "new_this_month": User.objects.filter(
                    role=User.Role.CUSTOMER, date_joined__gte=month_start
                ).count(),
            },
            "products": {
                "total": Product.objects.count(),
                "active": Product.objects.filter(is_active=True).count(),
                "out_of_stock": Product.objects.filter(
                    stock=0, track_inventory=True
                ).count(),
                "top_selling": list(top_products),
            },
            "categories": {"total": Category.objects.count()},
            "deals": {
                "active": Deal.objects.filter(
                    is_active=True, start_date__lte=now, end_date__gte=now
                ).count(),
            },
            "reviews": {
                "pending_approval": Review.objects.filter(is_approved=False).count(),
                "approved": Review.objects.filter(is_approved=True).count(),
            },
            "contact_messages": {
                "unresolved": ContactMessage.objects.filter(is_resolved=False).count()
            },
        }

        return Response(
            {"success": True, "message": "", "data": data}, status=status.HTTP_200_OK
        )
