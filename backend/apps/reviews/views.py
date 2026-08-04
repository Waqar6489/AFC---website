from rest_framework import permissions, viewsets

from apps.core.permissions import IsOwnerOrAdmin, IsVerifiedBuyer
from apps.notifications.models import AdminNotification
from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    filterset_fields = ["product", "rating"]
    throttle_scope = "review_submit"

    def get_queryset(self):
        queryset = Review.objects.select_related("user", "product")
        user = self.request.user
        product_id = self.request.query_params.get("product")

        if user.is_authenticated and (
            user.is_staff or getattr(user, "role", None) == "admin"
        ):
            return queryset  # admins see pending + approved for moderation

        # Public / customer view: only approved reviews, plus the user's
        # own pending reviews so they can see what they submitted.
        if user.is_authenticated:
            own = queryset.filter(user=user)
            approved = queryset.filter(is_approved=True)
            queryset = (own | approved).distinct()
        else:
            queryset = queryset.filter(is_approved=True)

        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsVerifiedBuyer()]
        if self.action in ("update", "partial_update", "destroy"):
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        return [permissions.AllowAny()]
    
    def perform_create(self, serializer):
        review = serializer.save(user=self.request.user)

        AdminNotification.objects.create(
        notification_type=AdminNotification.NotificationType.REVIEW,
        title="New Review",
        message=f"{review.user.full_name} reviewed {review.product.name}.")
