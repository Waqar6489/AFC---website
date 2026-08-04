from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.permissions import IsAdminOrReadOnly

from .models import Deal
from .serializers import CouponValidateSerializer, DealSerializer


class DealViewSet(viewsets.ModelViewSet):
    serializer_class = DealSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Deal.objects.all().prefetch_related("products", "categories")
        user = self.request.user
        if not (
            user.is_authenticated
            and (user.is_staff or getattr(user, "role", None) == "admin")
        ):
            now = timezone.now()
            queryset = queryset.filter(
                is_active=True, start_date__lte=now, end_date__gte=now
            )
        return queryset

    @action(detail=False, methods=["get"])
    def active(self, request):
        """Explicit endpoint for the homepage Deals section / Deals page —
        guaranteed to only return currently-running deals regardless of
        any other filtering."""
        now = timezone.now()
        queryset = Deal.objects.filter(
            is_active=True, start_date__lte=now, end_date__gte=now
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ValidateCouponView(APIView):
    """Public preview endpoint (cart page) — the same validation logic
    runs again, authoritatively, inside the checkout flow in apps.orders."""

    permission_classes = [permissions.AllowAny]
    throttle_scope = "contact_form"  # reuse a modest general-purpose rate limit

    def post(self, request):
        serializer = CouponValidateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        deal = serializer.validated_data["deal"]
        discount_amount = serializer.validated_data["discount_amount"]
        return Response(
            {
                "success": True,
                "message": "Coupon applied successfully.",
                "data": {
                    "coupon_code": deal.coupon_code,
                    "deal_title": deal.title,
                    "discount_amount": discount_amount,
                },
            },
            status=status.HTTP_200_OK,
        )
