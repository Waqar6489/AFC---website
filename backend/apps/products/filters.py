import django_filters as filters

from .models import Product


class ProductFilter(filters.FilterSet):
    """Powers the Shop page sidebar filters: category, price range, deal
    status, and availability, per spec."""

    category = filters.CharFilter(field_name="category__slug")
    min_price = filters.NumberFilter(method="filter_min_price")
    max_price = filters.NumberFilter(method="filter_max_price")
    on_deal = filters.BooleanFilter(method="filter_on_deal")
    in_stock = filters.BooleanFilter(method="filter_in_stock")
    is_trending = filters.BooleanFilter(field_name="is_trending")
    is_featured = filters.BooleanFilter(field_name="is_featured")
    is_best_seller = filters.BooleanFilter(field_name="is_best_seller")

    class Meta:
        model = Product
        fields = ["category", "is_trending", "is_featured", "is_best_seller"]

    def filter_min_price(self, queryset, name, value):
        from django.db.models import Case, F, When

        return queryset.annotate(
            _effective_price=Case(
                When(discount_price__isnull=False, then=F("discount_price")),
                default=F("price"),
            )
        ).filter(_effective_price__gte=value)

    def filter_max_price(self, queryset, name, value):
        from django.db.models import Case, F, When

        return queryset.annotate(
            _effective_price=Case(
                When(discount_price__isnull=False, then=F("discount_price")),
                default=F("price"),
            )
        ).filter(_effective_price__lte=value)

    def filter_on_deal(self, queryset, name, value):
        if value:
            return queryset.filter(discount_price__isnull=False)
        return queryset.filter(discount_price__isnull=True)

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset.filter(stock=0)
