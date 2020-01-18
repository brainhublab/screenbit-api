from rest_framework import serializers
from .models import Program
from ads.models import Ad
from ads.serializers import AdSerializer


class ProgramSerializer(serializers.HyperlinkedModelSerializer):
    """Media Program serializer"""

    class Meta:
        model = Program
        fields = ("id", "url", "creator", "creator_id", "title", "description",
                  "ad_ids", "media_urls", "created_at", "updated_at")
        read_only_fields = ("id", "url", "creator", "creator_id",
                            "created_at", "updated_at")
        required_fields = ("client" "title", "description", "ad_ids")
        extra_kwargs = {field: {"required": True} for field in required_fields}

    def get_current_user(self):
        """Gets current user from request"""
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            return user
        return None

    def validate_creator(self, value):
        """Validate creator field"""
        user = self.get_current_user()
        if user != value:
            raise serializers.VakidationError("You can not create services for another user")
        return value

    def create(self, validated_data):
        """Check are all ad exists and collect their urls"""
        media_urls = []
        if (self.context["request"]):
            request = self.context.get("request")
        for id in validated_data["ad_ids"]:
            ad = AdSerializer(many=False, instance=Ad.objects.filter(id=id).first(), context={'request': request}).data
            if ad:
                media_urls.append(dict(ad["file"][0])["file"])
            else:
                raise serializers.NotFound()
        validated_data["media_urls"] = media_urls
        program_data = super().create(validated_data)
        return program_data

    def update(self, instance, validated_data):
        """Check are all ad exists and collect their urls"""
        media_urls = []
        if (self.context["request"]):
            request = self.context.get("request")
        for id in validated_data["ad_ids"]:
            ad = AdSerializer(many=False, instance=Ad.objects.filter(id=id).first(), context={'request': request}).data
            if ad:
                media_urls.append(dict(ad["file"][0])["file"])
            else:
                raise serializers.NotFound()
        instance.media_urls = media_urls
        program_data = super().update(instance, validated_data)
        return program_data
