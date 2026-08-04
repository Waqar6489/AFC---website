from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.permissions import IsAdminOrReadOnly

from .filters import ProductFilter
from .models import Addon, Product
from .serializers import (
    AddonSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    ProductWriteSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
    filterset_class = ProductFilter
    search_fields = ["name", "description", "ingredients", "sku"]
    ordering_fields = ["price", "created_at", "average_rating", "name"]

    def get_queryset(self):
        queryset = Product.objects.select_related("category").prefetch_related(
            "images", "variants", "available_addons"
        )
        user = self.request.user
        if not (
            user.is_authenticated
            and (user.is_staff or getattr(user, "role", None) == "admin")
        ):
            queryset = queryset.filter(is_active=True)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        if self.action in ("create", "update", "partial_update"):
            return ProductWriteSerializer
        return ProductDetailSerializer

    @action(detail=False, methods=["get"])
    def trending(self, request):
        queryset = self.filter_queryset(self.get_queryset().filter(is_trending=True))
        page = self.paginate_queryset(queryset)
        serializer = ProductListSerializer(
            page or queryset, many=True, context={"request": request}
        )
        return (
            self.get_paginated_response(serializer.data)
            if page is not None
            else Response(serializer.data)
        )

    @action(detail=False, methods=["get"])
    def featured(self, request):
        queryset = self.filter_queryset(self.get_queryset().filter(is_featured=True))
        page = self.paginate_queryset(queryset)
        serializer = ProductListSerializer(
            page or queryset, many=True, context={"request": request}
        )
        return (
            self.get_paginated_response(serializer.data)
            if page is not None
            else Response(serializer.data)
        )

    @action(detail=False, methods=["get"], url_path="best-sellers")
    def best_sellers(self, request):
        queryset = self.filter_queryset(self.get_queryset().filter(is_best_seller=True))
        page = self.paginate_queryset(queryset)
        serializer = ProductListSerializer(
            page or queryset, many=True, context={"request": request}
        )
        return (
            self.get_paginated_response(serializer.data)
            if page is not None
            else Response(serializer.data)
        )


class AddonViewSet(viewsets.ModelViewSet):
    serializer_class = AddonSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["category", "is_active"]

    def get_queryset(self):
        queryset = Addon.objects.all()
        user = self.request.user
        if not (
            user.is_authenticated
            and (user.is_staff or getattr(user, "role", None) == "admin")
        ):
            queryset = queryset.filter(is_active=True)
        return queryset
