from rest_framework import viewsets

from apps.core.permissions import IsAdminOrReadOnly

from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Public read access; create/update/delete restricted to admin/staff.
    Public listing only shows active categories; admins see everything
    (needed to manage hidden/draft categories from Django Admin's sibling
    API views or an eventual admin dashboard)."""

    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
    filterset_fields = ["is_active"]
    search_fields = ["name", "description"]
    ordering_fields = ["order", "name", "created_at"]

    def get_queryset(self):
        queryset = Category.objects.all()
        user = self.request.user
        if not (
            user.is_authenticated
            and (user.is_staff or getattr(user, "role", None) == "admin")
        ):
            queryset = queryset.filter(is_active=True)
        return queryset
