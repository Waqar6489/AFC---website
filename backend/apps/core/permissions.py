"""Reusable, role-based DRF permission classes."""

from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """Allows access only to users with the admin/staff role."""

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_staff or getattr(user, "role", None) == "admin")
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """Object-level permission: only the owner of a record or an admin may
    view/edit it (e.g. orders, addresses, reviews, wishlist items)."""

    message = "You do not have permission to access this resource."

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_staff or getattr(user, "role", None) == "admin":
            return True
        owner = getattr(obj, "user", None) or getattr(obj, "customer", None)
        return owner == user


class IsVerifiedBuyer(permissions.BasePermission):
    """Used on review creation — only users who purchased & received the
    product may leave a review. The actual purchase check happens in the
    serializer (needs the product id), this just gates unauthenticated
    access early."""

    message = "Only verified buyers can submit a review."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class ReadOnly(permissions.BasePermission):
    """Allows only safe (GET/HEAD/OPTIONS) methods."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdminOrReadOnly(permissions.BasePermission):
    """Public read access, write access restricted to admin/staff — the
    standard permission for catalog data managed from Django Admin
    (categories, products, deals, FAQs, team members)."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_staff or getattr(user, "role", None) == "admin")
        )
