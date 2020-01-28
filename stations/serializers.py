from rest_framework import serializers
from .models import Station


class StationSerializer(serializers.HyperlinkedModelSerializer):
    """Station serializer"""

    class Meta:
        model = Station
        fields = ("id", "url", "creator", 'creator_id', "pprovider", "daily_program",
                  "title", "description", "city", "mac_addr", "net_addr", "p_addr",
                  "lat", "long", "created_at", "updated_at")

        read_only_fields = ("id", "url", "creator", 'creator_id', "pprovider",
                            "created_at", "updated_at")

        required_fields = ("title", "description", "mac_addr")
        extra_kwargs = {field: {"required": True} for field in required_fields}

    def get_current_user(self):
        """Gets Current user from request"""
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            return user
        return None

    def validate_creator(self, value):
        """Validate author field"""
        user = self.get_current_user()
        if user != value:
            raise serializers.ValidationError(
                ("You can not create services for another user"))
        return value

    def update(self, instance, validated_data):
        if not instance.daily_program:
            daily_program = super().update(instance, validated_data)
        else:
            if len(Station.objects.filter(daily_program=instance.daily_program)) == 1:
                instance.daily_program.is_in_use = False
                instance.daily_program.save()
            daily_program = super().update(instance, validated_data)
        return daily_program


class StationLocationSerializer(serializers.ModelSerializer):
    """Company Location Serializer
        Used tp return only companies locations data"""
    class Meta:
        model = Station
        fields = ("id", "lat", "long", "title")
        read_only_fields = fields
