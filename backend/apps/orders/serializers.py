from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from apps.accounts.models import Address
from apps.core.exceptions import BusinessLogicError
from apps.core.geo import is_within_delivery_radius
from apps.core.models import SiteConfiguration
from apps.deals.models import Deal
from apps.products.models import Product, ProductVariant
from datetime import time
from django.utils import timezone

from .models import Cart, CartItem, Order, OrderItem, OrderStatusHistory


# ------------------------------------------------------------------------------
# Cart
# ------------------------------------------------------------------------------
class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_slug = serializers.CharField(source="product.slug", read_only=True)
    product_image = serializers.SerializerMethodField()
    variant_size = serializers.CharField(
        source="variant.size", read_only=True, default=None
    )
    addon_details = serializers.SerializerMethodField()
    unit_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    line_total = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_slug",
            "product_image",
            "variant",
            "variant_size",
            "addons",
            "addon_details",
            "quantity",
            "notes",
            "unit_price",
            "line_total",
        ]
        read_only_fields = ["id"]

    def get_product_image(self, obj):
        request = self.context.get("request")

        image = (
        obj.product.images.filter(is_primary=True).first()
        or obj.product.images.first()
         )

        if image:
           return request.build_absolute_uri(image.image.url)

        return None

    def get_addon_details(self, obj):
        return [
            {"id": a.id, "name": a.name, "price": a.price} for a in obj.addons.all()
        ]

    def validate(self, attrs):
        product = attrs.get("product") or getattr(self.instance, "product", None)
        variant = attrs.get("variant", getattr(self.instance, "variant", None))
        addons = attrs.get("addons") or (self.instance.addons.all() if self.instance else None
)

        if variant and variant.product_id != product.id:
            raise serializers.ValidationError(
                {"variant": "This variant does not belong to the selected product."}
            )

        if product and product.variants.exists() and not variant:
            raise serializers.ValidationError(
                {"variant": "This product requires a size to be selected."}
            )

        if addons:
            valid_addon_ids = set(product.available_addons.values_list("id", flat=True))
            for addon in addons:
                if addon.id not in valid_addon_ids:
                    raise serializers.ValidationError(
                        {"addons": f"'{addon.name}' is not available for this product."}
                    )

        return attrs


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    item_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "items", "subtotal", "item_count", "updated_at"]


# ------------------------------------------------------------------------------
# Delivery eligibility
# ------------------------------------------------------------------------------
class DeliveryEligibilitySerializer(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)

    def validate_latitude(self, value):
        if not (-90 <= float(value) <= 90):
            raise serializers.ValidationError("Latitude must be between -90 and 90.")
        return value

    def validate_longitude(self, value):
        if not (-180 <= float(value) <= 180):
            raise serializers.ValidationError("Longitude must be between -180 and 180.")
        return value


# ------------------------------------------------------------------------------
# Checkout
# ------------------------------------------------------------------------------
class CheckoutSerializer(serializers.Serializer):
    """The authoritative checkout endpoint payload. Delivery radius is
    re-validated here server-side no matter what the frontend already
    checked — this is the check that cannot be bypassed."""

    address_id = serializers.UUIDField(required=False)

    full_name = serializers.CharField(max_length=150, required=False)
    phone = serializers.CharField(max_length=20, required=False)
    address_line = serializers.CharField(max_length=255, required=False)
    city = serializers.CharField(max_length=100, required=False)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False)
    save_address = serializers.BooleanField(default=False)

    coupon_code = serializers.CharField(required=False, allow_blank=True)
    notes = serializers.CharField(max_length=500, required=False, allow_blank=True)
    payment_method = serializers.ChoiceField(
        choices=Order.PaymentMethod.choices, default=Order.PaymentMethod.COD
    )

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user
        current_time = timezone.localtime().time()
        if current_time < time(8, 0) or current_time > time(23, 0):
             raise serializers.ValidationError({
                "order": "Orders are accepted only between 8:00 AM and 11:00 PM."
                  })

        # --- Resolve delivery address (existing saved address OR new inline one) ---
        address_id = attrs.get("address_id")
        if address_id:
            try:
                address = Address.objects.get(pk=address_id, user=user)
            except Address.DoesNotExist as exc:
                raise serializers.ValidationError(
                    {"address_id": "Address not found."}
                ) from exc
            attrs["_resolved_address"] = address
            lat, lon = address.latitude, address.longitude
        else:
            required_fields = [
                "full_name",
                "phone",
                "address_line",
                "city",
                "latitude",
                "longitude",
            ]
            missing = [f for f in required_fields if not attrs.get(f)]
            if missing:
                raise serializers.ValidationError(
                    {
                        "address_id": f"Provide an address_id or all of: {', '.join(required_fields)}."
                    }
                )
            attrs["_resolved_address"] = None
            lat, lon = attrs["latitude"], attrs["longitude"]

        # --- Authoritative delivery-radius check (Haversine formula) ---
        site_config = SiteConfiguration.load()
        within_radius, distance_km = is_within_delivery_radius(
            float(lat),
            float(lon),
            float(site_config.restaurant_latitude),
            float(site_config.restaurant_longitude),
            float(site_config.delivery_radius_km),
        )
        if not within_radius:
            raise BusinessLogicError(
                f"We currently deliver within {site_config.delivery_radius_km} KM of our restaurant. "
                f"Your location is {distance_km} KM away."
            )
        attrs["_distance_km"] = distance_km

        # --- Cart must exist and have items ---
        cart = getattr(user, "cart", None)
        if not cart or not cart.items.exists():
            raise serializers.ValidationError({"cart": "Your cart is empty."})
        attrs["_cart"] = cart

        # --- Stock check ---
        for item in cart.items.select_related("product", "variant"):
            available = item.variant.stock if item.variant else item.product.stock
            if item.product.track_inventory and available < item.quantity:
                raise serializers.ValidationError(
                    {
                        "cart": f"Only {available} of '{item.product.name}' left in stock."
                    }
                )

        # --- Coupon (optional) ---
        subtotal = cart.subtotal
        discount_amount = Decimal("0.00")
        deal = None
        coupon_code = (attrs.get("coupon_code") or "").strip().upper()
        if coupon_code:
            try:
                deal = Deal.objects.get(coupon_code__iexact=coupon_code)
            except Deal.DoesNotExist as exc:
                raise serializers.ValidationError(
                    {"coupon_code": "Invalid coupon code."}
                ) from exc
            if not deal.is_currently_active:
                raise serializers.ValidationError(
                    {"coupon_code": f"This coupon is {deal.status}."}
                )
            if subtotal < deal.min_order_amount:
                raise serializers.ValidationError(
                    {
                        "coupon_code": f"Minimum order amount for this coupon is {deal.min_order_amount}."
                    }
                )
            if deal.per_user_limit:
                usage_count = (
                    Order.objects.filter(user=user, coupon_code__iexact=coupon_code)
                    .exclude(status=Order.Status.CANCELLED)
                    .count()
                )
                if usage_count >= deal.per_user_limit:
                    raise serializers.ValidationError(
                        {"coupon_code": "You have already used this coupon."}
                    )
            discount_amount = deal.calculate_discount(subtotal)

        attrs["_deal"] = deal
        attrs["_subtotal"] = subtotal
        attrs["_discount_amount"] = discount_amount
        return attrs

    @transaction.atomic
    def save(self, **kwargs):
        user = self.context["request"].user
        data = self.validated_data
        cart: Cart = data["_cart"]

        address = data["_resolved_address"]
        if address is None:
            address = Address.objects.create(
                user=user,
                label=Address.Label.OTHER,
                full_name=data["full_name"],
                phone=data["phone"],
                address_line=data["address_line"],
                city=data["city"],
                latitude=data["latitude"],
                longitude=data["longitude"],
                is_default=data.get("save_address", False),
            )
        elif not data.get("save_address"):
            pass  # existing address, nothing to persist beyond what's already saved

        subtotal = data["_subtotal"]
        discount_amount = data["_discount_amount"]
        distance = Decimal(str(data["_distance_km"]))

        # Delivery Charges
        if subtotal >= Decimal("2000"):
            delivery_fee = Decimal("0.00")
        else:
            delivery_fee = distance * Decimal("30") 

        total_amount = max(
            subtotal + delivery_fee - discount_amount,
            Decimal("0.00")
        )
        deal = data["_deal"]

        order = Order.objects.create(
            user=user,
            address=address,
            delivery_full_name=address.full_name,
            delivery_phone=address.phone,
            delivery_address_line=address.address_line,
            delivery_city=address.city,
            delivery_latitude=address.latitude,
            delivery_longitude=address.longitude,
            distance_km=data["_distance_km"],
            notes=data.get("notes", ""),
            coupon_code=deal.coupon_code if deal else None,
            discount_amount=discount_amount,
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            total_amount=total_amount,
            payment_method=data["payment_method"],
        )

        for item in cart.items.select_related("product", "variant").prefetch_related(
            "addons"
        ):
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                variant_size=item.variant.get_size_display() if item.variant else "",
                addons_snapshot=[
                    {"name": a.name, "price": str(a.price)} for a in item.addons.all()
                ],
                unit_price=item.unit_price,
                quantity=item.quantity,
                line_total=item.line_total,
            )

            # Decrement stock
            if item.product.track_inventory:
                if item.variant:
                    ProductVariant.objects.filter(pk=item.variant.pk).update(
                        stock=item.variant.stock - item.quantity
                    )
                else:
                    Product.objects.filter(pk=item.product.pk).update(
                        stock=item.product.stock - item.quantity
                    )

        if deal:
            Deal.objects.filter(pk=deal.pk).update(used_count=deal.used_count + 1)

        OrderStatusHistory.objects.create(
            order=order, status=Order.Status.PENDING, note="Order placed."
        )

        cart.items.all().delete()

        return order


# ------------------------------------------------------------------------------
# Order read/update
# ------------------------------------------------------------------------------
class OrderItemReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "variant_size",
            "addons_snapshot",
            "unit_price",
            "quantity",
            "line_total",
        ]


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = ["status", "note", "changed_at"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "user_email",
            "items",
            "status_history",
            "delivery_full_name",
            "delivery_phone",
            "delivery_address_line",
            "delivery_city",
            "delivery_latitude",
            "delivery_longitude",
            "distance_km",
            "notes",
            "coupon_code",
            "discount_amount",
            "subtotal",
            "delivery_fee",
            "total_amount",
            "payment_method",
            "payment_status",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class OrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.Status.choices)
    note = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def save(self, **kwargs):
        order = self.context["order"]
        changed_by = self.context["request"].user
        order.status = self.validated_data["status"]
        order.save(update_fields=["status", "updated_at"])
        OrderStatusHistory.objects.create(
            order=order,
            status=order.status,
            changed_by=changed_by,
            note=self.validated_data.get("note", ""),
        )
        return order
