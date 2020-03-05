from rest_framework import serializers
from .models import Station
from django.conf import settings
from django.db.models.query import QuerySet

global_variables = settings.GLOBAL_VARIABLE[0]


class StationSerializer(serializers.HyperlinkedModelSerializer):
    """Station serializer"""

    class Meta:
        model = Station
        fields = ("id", "url", "creator", 'creator_id', "pprovider",
                  "ads", "title", "description", "city", "area", "viewers",
                  "mac_addr", "net_addr", "p_addr",
                  "lat", "long", "created_at", "updated_at")

        read_only_fields = ("id", "url", "creator", 'creator_id',
                            "created_at", "updated_at")

        required_fields = ("title", "description", "area", "viewers", "mac_addr")
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

    # def to_representation(self, instance, override=True):
    #     response = super().to_representation(instance)
    #     if not isinstance(self.instance, QuerySet):
    #         hourly_program = {}
    #         for relation in instance.stadrelation.all():
    #             if relation.hour not in hourly_program:
    #                 hourly_program[relation.hour] = {}
    #             hourly_program[relation.hour][relation.ad_index] = relation.ad.id
    #         response["hours"] = hourly_program
    #     return response


class StationLocationSerializer(serializers.ModelSerializer):
    """Company Location Serializer
        Used tp return only companies locations data"""
    class Meta:
        model = Station
        fields = ("id", "lat", "long", "title")
        read_only_fields = fields
