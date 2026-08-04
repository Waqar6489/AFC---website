from rest_framework import serializers

from apps.core.fields import ModelDefaultBooleanField

from .models import TeamMember


class TeamMemberSerializer(serializers.ModelSerializer):
    display_title = serializers.CharField(read_only=True)
    is_active = ModelDefaultBooleanField(default=True)
    image = serializers.SerializerMethodField()
    class Meta:
        model = TeamMember
        fields = [
            "id",
            "name",
            "position",
            "custom_title",
            "display_title",
            "bio",
            "image",
            "facebook_url",
            "instagram_url",
            "twitter_url",
            "linkedin_url",
            "order",
            "is_active",
        ]
        read_only_fields = ["id"]

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None    
