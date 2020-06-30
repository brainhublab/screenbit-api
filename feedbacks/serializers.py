from .models import Feedback
from rest_framework import serializers


class FeedbackSerializer(serializers.HyperlinkedModelSerializer):
    """Advertising serializer"""

    class Meta:
        model = Feedback
        fields = ("id", "url", "station", "station_id",
                  "ad", "ad_id", "area", "hour", "viewers",
                  "holders", "button_usrs", "reached",
                  "created_at", "updated_at", )
        read_only_fields = ("id", "url", "created_at", "updated_at", )
        required_fields = ("stataion", "ad", "hour", )
        extra_kwargs = {field: {"required": True} for field in required_fields}
