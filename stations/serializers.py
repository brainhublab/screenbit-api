from rest_framework import serializers
from .models import Station, StationProgramRelation
from programs.models import Program
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet

global_variables = settings.GLOBAL_VARIABLE[0]


class StationSerializer(serializers.HyperlinkedModelSerializer):
    """Station serializer"""

    class Meta:
        model = Station
        fields = ("id", "url", "creator", 'creator_id', "pprovider",
                  "programs", "title", "description", "city", "area", "viewers",
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

    def _custom_relations_schema_validator(self):
        request_data = self.context.get("request").data
        if "relations_schema" in request_data:
            relations_schema = request_data["relations_schema"]
            if relations_schema is not None:
                for hour in relations_schema:
                    if hour not in global_variables["available_hours_choices"]:
                        raise serializers.ValidationError({"message": "Unavailable key in relations_schema"})
                    get_object_or_404(Program, id=relations_schema[hour])
        if "programs" in request_data:
            del request_data["programs"]
        return request_data

    def create(self, validated_data):
        request_data = self._custom_relations_schema_validator()
        station = super().create(validated_data)
        for hour in request_data["relations_schema"]:
            StationProgramRelation(program=Program.objects.get(id=request_data["relations_schema"][hour]),
                                   station=station,
                                   hour=hour).save()
        return station

    def update(self, instance, validated_data):
        request_data = self._custom_relations_schema_validator()
        station = super().update(instance, validated_data)
        if request_data["relations_schema"] is None:
            instance.programs.clear()
            return station
        else:
            instance.programs.clear()
            for hour in request_data["relations_schema"]:
                StationProgramRelation(program=Program.objects.get(id=request_data["relations_schema"][hour]),
                                       station=station,
                                       hour=hour).save()
        return station

    def to_representation(self, instance, override=True):
        response = super().to_representation(instance)
        if not isinstance(self.instance, QuerySet):
            programs = {}
            for relation in instance.stprrelation.all():
                programs[relation.hour] = {}
                programs[relation.hour]["program_id"] = relation.program.id
                ads_relations = {}
                for program_relation in relation.program.pradmembership.all():
                    ads_relations[program_relation.ad_index] = program_relation.ad.id
                programs[relation.hour]["program_ads"] = ads_relations
            response["hours"] = programs
        return response


class StationLocationSerializer(serializers.ModelSerializer):
    """Company Location Serializer
        Used tp return only companies locations data"""
    class Meta:
        model = Station
        fields = ("id", "lat", "long", "title")
        read_only_fields = fields
