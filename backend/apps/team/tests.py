import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

pytestmark = pytest.mark.django_db


def _tiny_valid_jpeg():
    from io import BytesIO

    from PIL import Image

    buffer = BytesIO()
    Image.new("RGB", (10, 10), color="yellow").save(buffer, format="JPEG")
    buffer.seek(0)
    return SimpleUploadedFile("test.jpg", buffer.read(), content_type="image/jpeg")


class TestTeamMember:
    def test_public_only_sees_active_members(self, api_client):
        from apps.team.models import TeamMember

        TeamMember.objects.create(
            name="Visible", position="chef", image=_tiny_valid_jpeg(), is_active=True
        )
        TeamMember.objects.create(
            name="Hidden", position="staff", image=_tiny_valid_jpeg(), is_active=False
        )

        response = api_client.get(reverse("team-member-list"))
        names = [m["name"] for m in response.data["results"]]
        assert "Visible" in names
        assert "Hidden" not in names

    def test_create_via_multipart_defaults_is_active_true(
        self, api_client, auth_client, user_factory
    ):
        """Regression test: multipart/form-data submissions (required for
        the image upload) must not silently force is_active to False when
        the field is omitted — it should fall back to the model default."""
        admin = user_factory(email="teamadmin@example.com", role="admin", is_staff=True)
        auth_client(api_client, admin)

        response = api_client.post(
            reverse("team-member-list"),
            {
                "name": "Ahmad Raza",
                "position": "owner",
                "bio": "Founder.",
                "image": _tiny_valid_jpeg(),
            },
            format="multipart",
        )
        assert response.status_code == 201
        assert response.data["is_active"] is True

        from apps.team.models import TeamMember

        assert TeamMember.objects.get(pk=response.data["id"]).is_active is True

    def test_display_title_falls_back_to_position(self, api_client):
        from apps.team.models import TeamMember

        member = TeamMember.objects.create(
            name="Chef X", position="chef", image=_tiny_valid_jpeg()
        )
        response = api_client.get(
            reverse("team-member-detail", kwargs={"pk": member.pk})
        )
        assert response.data["display_title"] == "Chef"
