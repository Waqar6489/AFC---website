import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestProductList:
    def test_list_only_active_products_publicly(self, api_client, product_factory):
        product_factory(name="Active Cake", is_active=True)
        product_factory(name="Hidden Cake", is_active=False)
        response = api_client.get(reverse("product-list"))
        assert response.status_code == 200
        names = [p["name"] for p in response.data["results"]]
        assert "Active Cake" in names
        assert "Hidden Cake" not in names

    def test_filter_by_category_slug(
        self, api_client, category_factory, product_factory
    ):
        cakes = category_factory(name="Cakes")
        pastries = category_factory(name="Pastries")
        product_factory(name="Cake A", category=cakes)
        product_factory(name="Pastry A", category=pastries)

        response = api_client.get(reverse("product-list"), {"category": "cakes"})
        names = [p["name"] for p in response.data["results"]]
        assert names == ["Cake A"]

    def test_filter_by_price_range(self, api_client, product_factory):
        product_factory(name="Cheap", price=100)
        product_factory(name="Expensive", price=5000)

        response = api_client.get(
            reverse("product-list"), {"min_price": 50, "max_price": 200}
        )
        names = [p["name"] for p in response.data["results"]]
        assert names == ["Cheap"]

    def test_search_by_name(self, api_client, product_factory):
        product_factory(name="Red Velvet Cake")
        product_factory(name="Vanilla Cupcake")
        response = api_client.get(reverse("product-list"), {"search": "Velvet"})
        names = [p["name"] for p in response.data["results"]]
        assert names == ["Red Velvet Cake"]

    def test_trending_endpoint(self, api_client, product_factory):
        product_factory(name="Trending Item", is_trending=True)
        product_factory(name="Normal Item", is_trending=False)
        response = api_client.get(reverse("product-trending"))
        names = [p["name"] for p in response.data["results"]]
        assert names == ["Trending Item"]


class TestProductDetail:
    def test_detail_includes_variants_and_addons(
        self, api_client, product_factory, variant_factory, addon_factory
    ):
        product = product_factory()
        variant_factory(product, size="small", price=800)
        variant_factory(product, size="large", price=1500)
        addon = addon_factory()
        product.available_addons.add(addon)

        response = api_client.get(
            reverse("product-detail", kwargs={"slug": product.slug})
        )
        assert response.status_code == 200
        assert len(response.data["variants"]) == 2
        assert response.data["available_addons"][0]["name"] == addon.name

    def test_effective_price_uses_discount(self, api_client, product_factory):
        product = product_factory(price=1000, discount_price=800)
        response = api_client.get(
            reverse("product-detail", kwargs={"slug": product.slug})
        )
        assert response.data["effective_price"] == "800.00"
        assert response.data["discount_percentage"] == 20

    def test_related_products_falls_back_to_same_category(
        self, api_client, category_factory, product_factory
    ):
        cat = category_factory()
        p1 = product_factory(name="Main", category=cat)
        product_factory(name="Sibling", category=cat)

        response = api_client.get(reverse("product-detail", kwargs={"slug": p1.slug}))
        related_names = [p["name"] for p in response.data["related_products"]]
        assert "Sibling" in related_names


class TestProductWritePermissions:
    def test_anonymous_cannot_create_product(self, api_client, category_factory):
        category = category_factory()
        response = api_client.post(
            reverse("product-list"),
            {
                "category": category.id,
                "name": "New",
                "sku": "NEW-1",
                "description": "x",
                "price": 100,
            },
        )
        assert response.status_code in (401, 403)

    def test_admin_can_create_product(
        self, api_client, auth_client, user_factory, category_factory
    ):
        admin = user_factory(email="admin2@example.com", role="admin", is_staff=True)
        auth_client(api_client, admin)
        category = category_factory()
        response = api_client.post(
            reverse("product-list"),
            {
                "category": category.id,
                "name": "Admin Created",
                "sku": "ADM-1",
                "description": "x",
                "price": 100,
            },
        )
        assert response.status_code == 201
