from rest_framework import serializers

from apps.orders.models import Order, OrderItem

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)
    user_avatar = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "product",
            "user_name",
            "user_avatar",
            "order",
            "rating",
            "comment",
            "image",
            "is_verified_purchase",
            "is_approved",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "is_verified_purchase",
            "is_approved",
            "created_at",
            "user_name",
            "user_avatar",
        ]
    def get_user_avatar(self, obj):
        if obj.user.avatar:
            return obj.user.avatar.url
        return None    

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user
        product = attrs["product"]
        order = attrs.get("order")

        # Verified-buyer gate: the order must belong to the user, contain
        # this product, and be marked Delivered.
        if not order:
            order = (
                Order.objects.filter(
                    user=user, status=Order.Status.DELIVERED, items__product=product
                )
                .order_by("-created_at")
                .first()
            )
            if not order:
                raise serializers.ValidationError(
                    "Only verified buyers who have received this product can submit a review."
                )
            attrs["order"] = order
        else:
            if order.user_id != user.id:
                raise serializers.ValidationError(
                    {"order": "This order does not belong to you."}
                )
            if order.status != Order.Status.DELIVERED:
                raise serializers.ValidationError(
                    {"order": "This order has not been delivered yet."}
                )
            if not OrderItem.objects.filter(order=order, product=product).exists():
                raise serializers.ValidationError(
                    {"order": "This product was not part of the selected order."}
                )

        if Review.objects.filter(
            product=product, user=user, order=attrs["order"]
        ).exists():
            raise serializers.ValidationError(
                "You have already reviewed this product for this order."
            )

        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        validated_data["is_verified_purchase"] = True
        validated_data["is_approved"] = False  # always requires admin approval
        return super().create(validated_data)
    
