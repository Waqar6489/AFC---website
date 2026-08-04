import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def _auth(api_client, user):
    from rest_framework_simplejwt.tokens import RefreshToken

    token = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")


class TestProfile:
    def test_get_own_profile(self, api_client, user_factory):
        user = user_factory(email="profile@example.com")
        _auth(api_client, user)
        response = api_client.get(reverse("profile"))
        assert response.status_code == 200
        assert response.data["email"] == "profile@example.com"

    def test_update_profile(self, api_client, user_factory):
        user = user_factory(email="update@example.com")
        _auth(api_client, user)
        response = api_client.patch(
            reverse("profile"), {"first_name": "Updated"}, format="json"
        )
        assert response.status_code == 200
        user.refresh_from_db()
        assert user.first_name == "Updated"

    def test_cannot_change_own_role(self, api_client, user_factory):
        user = user_factory(email="norole@example.com")
        _auth(api_client, user)
        api_client.patch(reverse("profile"), {"role": "admin"}, format="json")
        user.refresh_from_db()
        assert user.role == "customer"

    def test_profile_requires_auth(self, api_client):
        response = api_client.get(reverse("profile"))
        assert response.status_code == 401


class TestAddresses:
    def test_create_and_list_address(self, api_client, user_factory):
        user = user_factory(email="addr@example.com")
        _auth(api_client, user)
        payload = {
            "label": "home",
            "full_name": "Test User",
            "phone": "+923001234567",
            "address_line": "Street 1",
            "city": "Islamabad",
            "latitude": 33.6844,
            "longitude": 73.0479,
            "is_default": True,
        }
        create_response = api_client.post(
            reverse("address-list"), payload, format="json"
        )
        assert create_response.status_code == 201

        list_response = api_client.get(reverse("address-list"))
        assert list_response.status_code == 200
        assert list_response.data["count"] == 1

    def test_address_scoped_to_owner(self, api_client, user_factory):
        user_a = user_factory(email="ownera@example.com")
        user_b = user_factory(email="ownerb@example.com")

        _auth(api_client, user_a)
        api_client.post(
            reverse("address-list"),
            {
                "label": "home",
                "full_name": "A",
                "phone": "+923001234567",
                "address_line": "St A",
                "city": "Islamabad",
                "latitude": 33.6844,
                "longitude": 73.0479,
            },
            format="json",
        )

        _auth(api_client, user_b)
        response = api_client.get(reverse("address-list"))
        assert response.data["count"] == 0

    def test_invalid_latitude_rejected(self, api_client, user_factory):
        user = user_factory(email="badlat@example.com")
        _auth(api_client, user)
        response = api_client.post(
            reverse("address-list"),
            {
                "label": "home",
                "full_name": "Test",
                "phone": "+923001234567",
                "address_line": "St",
                "city": "Islamabad",
                "latitude": 999,
                "longitude": 73.0479,
            },
            format="json",
        )
        assert response.status_code == 400


class TestWishlist:
    def test_add_and_list_wishlist_item(
        self, api_client, user_factory, product_factory
    ):
        user = user_factory(email="wish1@example.com")
        _auth(api_client, user)
        product = product_factory()

        create_response = api_client.post(
            reverse("wishlist-list"), {"product": product.id}
        )
        assert create_response.status_code == 201

        list_response = api_client.get(reverse("wishlist-list"))
        assert list_response.data["count"] == 1
        assert list_response.data["results"][0]["product_name"] == product.name

    def test_cannot_add_duplicate(self, api_client, user_factory, product_factory):
        user = user_factory(email="wish2@example.com")
        _auth(api_client, user)
        product = product_factory()
        api_client.post(reverse("wishlist-list"), {"product": product.id})
        response = api_client.post(reverse("wishlist-list"), {"product": product.id})
        assert response.status_code == 400

    def test_wishlist_scoped_to_owner(self, api_client, user_factory, product_factory):
        user_a = user_factory(email="wisha@example.com")
        user_b = user_factory(email="wishb@example.com")
        product = product_factory()

        _auth(api_client, user_a)
        api_client.post(reverse("wishlist-list"), {"product": product.id})

        _auth(api_client, user_b)
        response = api_client.get(reverse("wishlist-list"))
        assert response.data["count"] == 0

    def test_remove_wishlist_item(self, api_client, user_factory, product_factory):
        user = user_factory(email="wish3@example.com")
        _auth(api_client, user)
        product = product_factory()
        create_response = api_client.post(
            reverse("wishlist-list"), {"product": product.id}
        )
        item_id = create_response.data["id"]

        delete_response = api_client.delete(
            reverse("wishlist-detail", kwargs={"pk": item_id})
        )
        assert delete_response.status_code == 204
        assert api_client.get(reverse("wishlist-list")).data["count"] == 0
