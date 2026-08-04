from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response

from apps.core.permissions import IsOwnerOrAdmin

from .models import Address, WishlistItem
from .serializers import (
    AddressSerializer,
    UserProfileSerializer,
    WishlistItemSerializer,
)


class ProfileView(generics.RetrieveUpdateAPIView):
    """GET/PATCH the authenticated user's own profile."""

    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": True,
                "message": "Profile updated successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class AddressViewSet(viewsets.ModelViewSet):
    """Full CRUD for a customer's saved delivery addresses. Scoped strictly
    to the requesting user — admins can see all via the Django Admin
    instead of this customer-facing endpoint."""

    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WishlistViewSet(viewsets.ModelViewSet):
    """Full CRUD for a customer's wishlist. Scoped strictly to the
    requesting user."""

    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "delete", "head", "options"]

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user).select_related(
            "product"
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
