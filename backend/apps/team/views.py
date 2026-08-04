from rest_framework import viewsets

from apps.core.permissions import IsAdminOrReadOnly

from .models import TeamMember
from .serializers import TeamMemberSerializer


class TeamMemberViewSet(viewsets.ModelViewSet):
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["position"]

    def get_queryset(self):
        queryset = TeamMember.objects.all()
        user = self.request.user
        if not (
            user.is_authenticated
            and (user.is_staff or getattr(user, "role", None) == "admin")
        ):
            queryset = queryset.filter(is_active=True)
        return queryset
