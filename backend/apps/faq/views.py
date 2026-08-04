from rest_framework import viewsets

from apps.core.permissions import IsAdminOrReadOnly

from .models import FAQ
from .serializers import FAQSerializer


class FAQViewSet(viewsets.ModelViewSet):
    serializer_class = FAQSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering_fields = ["order", "created_at"]

    def get_queryset(self):
        queryset = FAQ.objects.all()
        user = self.request.user
        if not (
            user.is_authenticated
            and (user.is_staff or getattr(user, "role", None) == "admin")
        ):
            queryset = queryset.filter(is_active=True)
        return queryset
