from rest_framework import serializers

from .models import Address, User, WishlistItem


class UserProfileSerializer(serializers.ModelSerializer):
    """Read/update serializer for the authenticated user's own profile.
    Email and role are intentionally read-only here — email changes go
    through a separate verification flow, role changes are admin-only."""

    full_name = serializers.CharField(source="get_full_name", read_only=True)
    avatar = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "phone",
            "avatar",
            "role",
            "is_email_verified",
            "date_joined",
        ]
        read_only_fields = ["id", "email", "role", "is_email_verified", "date_joined"]
    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None    


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "label",
            "full_name",
            "phone",
            "address_line",
            "city",
            "state",
            "postal_code",
            "country",
            "latitude",
            "longitude",
            "is_default",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_latitude(self, value):
        if not (-90 <= float(value) <= 90):
            raise serializers.ValidationError("Latitude must be between -90 and 90.")
        return value

    def validate_longitude(self, value):
        if not (-180 <= float(value) <= 180):
            raise serializers.ValidationError("Longitude must be between -180 and 180.")
        return value

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class AdminUserListSerializer(serializers.ModelSerializer):
    """Slim serializer used in the admin users list / CSV export."""

    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "phone",
            "role",
            "is_active",
            "is_email_verified",
            "date_joined",
        ]


class WishlistItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_slug = serializers.CharField(source="product.slug", read_only=True)
    product_price = serializers.DecimalField(
        source="product.effective_price",
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )
    product_image = serializers.SerializerMethodField()
    in_stock = serializers.BooleanField(source="product.in_stock", read_only=True)

    class Meta:
        model = WishlistItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_slug",
            "product_price",
            "product_image",
            "in_stock",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def get_product_image(self, obj):
        image = (
            obj.product.images.filter(is_primary=True).first()
            or obj.product.images.first()
        )
        return image.image.url if image else None

    def validate_product(self, value):
        user = self.context["request"].user
        if WishlistItem.objects.filter(user=user, product=value).exists():
            raise serializers.ValidationError(
                "This product is already in your wishlist."
            )
        return value

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
