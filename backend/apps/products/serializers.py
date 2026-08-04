from rest_framework import serializers

from apps.categories.serializers import CategorySerializer
from apps.core.fields import ModelDefaultBooleanField

from .models import Addon, Product, ProductImage, ProductVariant


class AddonSerializer(serializers.ModelSerializer):
    is_active = ModelDefaultBooleanField(default=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Addon
        fields = ["id", "name", "category", "price", "image", "is_active"]
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None    


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ["id", "size", "price", "stock"]


class ProductImageSerializer(serializers.ModelSerializer):
    image= serializers.SerializerMethodField()
    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt_text", "is_primary", "order"]
        def get_image(self, obj):
            if obj.image:
                return obj.image.url
            return None


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for grid/list views (shop page, home page
    sections) — avoids pulling the full gallery/variant/addon payload for
    every card."""

    category = serializers.CharField(source="category.name", read_only=True)
    category_slug = serializers.CharField(source="category.slug", read_only=True)
    primary_image = serializers.SerializerMethodField()
    effective_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    discount_percentage = serializers.IntegerField(read_only=True)
    in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "short_description",
            "category",
            "category_slug",
            "primary_image",
            "price",
            "discount_price",
            "effective_price",
            "discount_percentage",
            "in_stock",
            "is_trending",
            "is_featured",
            "is_best_seller",
            "average_rating",
            "review_count",
        ]

    def get_primary_image(self, obj):
        image = obj.images.filter(is_primary=True).first() or obj.images.first()
        if image:
            request = self.context.get("request")
            url = image.image.url
            return request.build_absolute_uri(url) if request else url
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    available_addons = AddonSerializer(many=True, read_only=True)
    related_products = serializers.SerializerMethodField()
    frequently_bought_with = ProductListSerializer(many=True, read_only=True)
    effective_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    discount_percentage = serializers.IntegerField(read_only=True)
    in_stock = serializers.BooleanField(read_only=True)
    nutrition = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "short_description",
            "description",
            "ingredients",
            "category",
            "sku",
            "price",
            "discount_price",
            "effective_price",
            "discount_percentage",
            "stock",
            "in_stock",
            "variants",
            "images",
            "available_addons",
            "related_products",
            "frequently_bought_with",
            "nutrition",
            "is_trending",
            "is_featured",
            "is_best_seller",
            "average_rating",
            "review_count",
            "created_at",
        ]

    def get_nutrition(self, obj):
        return {
            "calories": obj.calories,
            "protein_g": obj.protein_g,
            "carbs_g": obj.carbs_g,
            "fat_g": obj.fat_g,
            "sugar_g": obj.sugar_g,
        }

    def get_related_products(self, obj):
        queryset = obj.related_products.filter(is_active=True)
        if not queryset.exists():
            queryset = Product.objects.filter(
                category=obj.category, is_active=True
            ).exclude(pk=obj.pk)[:8]
        return ProductListSerializer(queryset, many=True, context=self.context).data
    def get_images(self, obj):
       images = obj.images.all()
       request = self.context.get("request")
       return [
        request.build_absolute_uri(image.image.url) if request else image.image.url
        for image in images
    ]

class ProductWriteSerializer(serializers.ModelSerializer):
    """Used by admin CRUD operations against the API (in addition to
    Django Admin). Variants/images/addons are managed through their own
    nested endpoints or Django Admin inlines, not through this payload."""

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "short_description",
            "description",
            "ingredients",
            "calories",
            "protein_g",
            "carbs_g",
            "fat_g",
            "sugar_g",
            "sku",
            "barcode",
            "price",
            "discount_price",
            "stock",
            "track_inventory",
            "available_addons",
            "related_products",
            "frequently_bought_with",
            "is_active",
            "is_trending",
            "is_featured",
            "is_best_seller",
        ]
        read_only_fields = ["id"]
