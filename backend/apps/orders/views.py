from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.geo import is_within_delivery_radius
from apps.core.models import SiteConfiguration
from apps.core.permissions import IsAdminRole, IsOwnerOrAdmin
from apps.notifications.models import AdminNotification

from .models import Cart, CartItem, Order
from .serializers import (
    CartItemSerializer,
    CartSerializer,
    CheckoutSerializer,
    DeliveryEligibilitySerializer,
    OrderSerializer,
    OrderStatusUpdateSerializer,
)


class CartView(generics.RetrieveAPIView):
    """Returns (and lazily creates) the authenticated user's cart."""

    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, _created = Cart.objects.get_or_create(user=self.request.user)
        return cart


class CartItemViewSet(viewsets.ModelViewSet):
    """Add/update/remove individual cart line items. Scoped strictly to
    the authenticated user's own cart."""

    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cart, _created = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def perform_create(self, serializer):
        cart, _created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)


class DeliveryEligibilityView(APIView):
    """Lightweight pre-checkout check the frontend calls right after the
    browser Geolocation API returns coordinates, to enable/disable the
    checkout button before the user fills in the rest of the form. The
    real, unbypassable check happens again inside CheckoutView."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = DeliveryEligibilitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        site_config = SiteConfiguration.load()
       
        within_radius, distance_km = is_within_delivery_radius(
            float(serializer.validated_data["latitude"]),
            float(serializer.validated_data["longitude"]),
            float(site_config.restaurant_latitude),
            float(site_config.restaurant_longitude),
            float(site_config.delivery_radius_km),
        )
        return Response(
            {
                "success": True,
                "message": (
                    ""
                    if within_radius
                    else f"We currently deliver within {site_config.delivery_radius_km} KM of our restaurant."
                ),
                "data": {
                    "is_within_radius": within_radius,
                    "distance_km": distance_km,
                    "delivery_radius_km": float(site_config.delivery_radius_km),
                },
            },
            status=status.HTTP_200_OK,
        )


class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "auth"

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        AdminNotification.objects.create(
        notification_type=AdminNotification.NotificationType.ORDER,
        title="New Order",
        message=f"New order #{order.order_number} received.")
        return Response(
            {
                "success": True,
                "message": "Order placed successfully.",
                "data": OrderSerializer(order).data,
            },
            status=status.HTTP_201_CREATED,
        )


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """Customers see only their own orders; admin/staff see everything
    and can transition order status via the `update_status` action."""

    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    lookup_field = "order_number"
    filterset_fields = ["status", "payment_status"]

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.all().prefetch_related("items", "status_history")
        if user.is_staff or getattr(user, "role", None) == "admin":
            return queryset
        return queryset.filter(user=user)

    def get_permissions(self):
        if self.action == "update_status":
            return [permissions.IsAuthenticated(), IsAdminRole()]
        return super().get_permissions()

    @action(detail=True, methods=["post"], url_path="update-status")
    def update_status(self, request, order_number=None):
        order = self.get_object()
        serializer = OrderStatusUpdateSerializer(
            data=request.data, context={"order": order, "request": request}
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(
            {
                "success": True,
                "message": "Order status updated.",
                "data": OrderSerializer(order).data,
            },
            status=status.HTTP_200_OK,
        )
