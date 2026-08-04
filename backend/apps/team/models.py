from django.db import models

from apps.core.models import TimeStampedModel
from cloudinary.models import CloudinaryField

class TeamMember(TimeStampedModel):
    """A team member shown on the About Us page — owner, chef, manager,
    or staff, per spec. Fully manageable from Django Admin."""

    class Position(models.TextChoices):
        OWNER = "owner", "Owner"
        CHEF = "chef", "Chef"
        MANAGER = "manager", "Manager"
        STAFF = "staff", "Staff"

    name = models.CharField(max_length=150)
    position = models.CharField(max_length=10, choices=Position.choices)
    custom_title = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional — overrides the display label, e.g. 'Head Pastry Chef'.",
    )
    bio = models.TextField(blank=True)
    image = CloudinaryField("Team_Member_Image", blank=True, null=True)

    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} ({self.display_title})"

    @property
    def display_title(self):
        return self.custom_title or self.get_position_display()
