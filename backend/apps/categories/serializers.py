from rest_framework import serializers

from apps.core.fields import ModelDefaultBooleanField

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    product_count = serializers.SerializerMethodField()
    is_active = ModelDefaultBooleanField(default=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "image",
            "order",
            "is_active",
            "product_count",
        ]
        read_only_fields = ["id", "slug"]

    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None
