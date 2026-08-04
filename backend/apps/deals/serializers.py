from decimal import Decimal, InvalidOperation

from rest_framework import serializers

from .models import Deal


class DealSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    seconds_remaining = serializers.SerializerMethodField()
    product_ids = serializers.PrimaryKeyRelatedField(
        source="products", many=True, read_only=True
    )
    category_ids = serializers.PrimaryKeyRelatedField(
        source="categories", many=True, read_only=True
    )
    banner_image = serializers.SerializerMethodField() 
    class Meta:
        model = Deal
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "banner_image",
            "discount_type",
            "discount_value",
            "max_discount_amount",
            "min_order_amount",
            "coupon_code",
            "product_ids",
            "category_ids",
            "start_date",
            "end_date",
            "status",
            "seconds_remaining",
        ]

    def get_seconds_remaining(self, obj):
        from django.utils import timezone

        if obj.status != Deal.Status.ACTIVE:
            return 0
        delta = obj.end_date - timezone.now()
        return max(int(delta.total_seconds()), 0)
    def get_banner_image(self, obj):
        if obj.banner_image:
            return obj.banner_image.url
        return None


class CouponValidateSerializer(serializers.Serializer):
    """Validates a coupon code against a given cart subtotal — used both
    at the cart page (preview) and re-validated server-side at checkout."""

    code = serializers.CharField()
    order_amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, attrs):
        code = attrs["code"].strip().upper()
        try:
            deal = Deal.objects.get(coupon_code__iexact=code)
        except Deal.DoesNotExist as exc:
            raise serializers.ValidationError({"code": "Invalid coupon code."}) from exc

        if not deal.is_currently_active:
            raise serializers.ValidationError(
                {"code": f"This coupon is {deal.status}."}
            )

        if attrs["order_amount"] < deal.min_order_amount:
            raise serializers.ValidationError(
                {
                    "order_amount": f"Minimum order amount for this coupon is {deal.min_order_amount}."
                }
            )

        user = self.context["request"].user
        if user.is_authenticated and deal.per_user_limit:
            from apps.orders.models import Order

            usage_count = (
                Order.objects.filter(user=user, coupon_code__iexact=code)
                .exclude(status=Order.Status.CANCELLED)
                .count()
            )
            if usage_count >= deal.per_user_limit:
                raise serializers.ValidationError(
                    {
                        "code": "You have already used this coupon the maximum number of times."
                    }
                )

        attrs["deal"] = deal
        try:
            attrs["discount_amount"] = deal.calculate_discount(
                Decimal(attrs["order_amount"])
            )
        except InvalidOperation as exc:
            raise serializers.ValidationError(
                {"order_amount": "Invalid amount."}
            ) from exc
        return attrs
