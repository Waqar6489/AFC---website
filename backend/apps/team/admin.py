from django.contrib import admin
from django.utils.html import format_html

from .models import TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        "thumbnail",
        "name",
        "position",
        "display_title",
        "order",
        "is_active",
    )
    list_editable = ("order", "is_active")
    list_filter = ("position", "is_active")
    search_fields = ("name", "bio")
    ordering = ("order",)

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:50%;" />',
                obj.image.url,
            )
        return "—"

    thumbnail.short_description = "Photo"
