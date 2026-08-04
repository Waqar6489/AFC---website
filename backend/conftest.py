import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_factory(db):
    from apps.accounts.models import User

    def _create(email="user@example.com", password="TestPass123!", **kwargs):
        return User.objects.create_user(
            email=email, password=password, first_name="Test", **kwargs
        )

    return _create


def _auth(api_client, user):
    from rest_framework_simplejwt.tokens import RefreshToken

    token = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
    return api_client


@pytest.fixture
def auth_client():
    return _auth


@pytest.fixture
def site_config(db):
    """Restaurant at Islamabad F-8 (33.7077, 73.0498), 10 KM radius —
    matches the coordinates used throughout the test suite."""
    from apps.core.models import SiteConfiguration

    config = SiteConfiguration.load()
    config.restaurant_latitude = 33.7077
    config.restaurant_longitude = 73.0498
    config.delivery_radius_km = 10
    config.save()
    return config


@pytest.fixture
def category_factory(db):
    from django.core.files.base import ContentFile

    from apps.categories.models import Category

    def _create(name="Cakes", **kwargs):
        cat = Category(name=name, **kwargs)
        cat.image.save("test.jpg", ContentFile(b"fake-image-bytes"), save=True)
        return cat

    return _create


@pytest.fixture
def product_factory(db, category_factory):
    from apps.products.models import Product

    default_category = {}

    def _create(
        name="Chocolate Fudge Cake",
        sku=None,
        category=None,
        price=1200,
        stock=50,
        **kwargs,
    ):
        if category is None:
            if "default" not in default_category:
                default_category["default"] = category_factory()
            category = default_category["default"]
        sku = sku or f"SKU-{name[:5].upper()}-{Product.objects.count() + 1}"
        return Product.objects.create(
            category=category,
            name=name,
            sku=sku,
            description="A delicious product.",
            price=price,
            stock=stock,
            **kwargs,
        )

    return _create


@pytest.fixture
def variant_factory(db):
    from apps.products.models import ProductVariant

    def _create(product, size="small", price=800, stock=20):
        return ProductVariant.objects.create(
            product=product, size=size, price=price, stock=stock
        )

    return _create


@pytest.fixture
def addon_factory(db):
    from apps.products.models import Addon

    def _create(name="Extra Cheese", category="cheese", price=100):
        return Addon.objects.create(name=name, category=category, price=price)

    return _create
