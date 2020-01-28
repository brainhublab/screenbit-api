from rest_framework import serializers
from .models import Program, ProgramAdMembership
from ads.models import Ad
from django.shortcuts import get_object_or_404


class ProgramSerializer(serializers.HyperlinkedModelSerializer):
    """Media Program serializer"""

    class Meta:
        model = Program
        fields = ("id", "url", "creator", "creator_id", "title", "description",
                  "ad_members", "created_at", "updated_at")
        read_only_fields = ("id", "url", "creator", "creator_id",
                            "created_at", "updated_at")
        required_fields = ("client", "title", "description")
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
            raise serializers.ValidationError("You can not create services for another user")
        return value

    def _cistom_order_schema_validator(self):
        request_data = self.context.get("request").data
        if "ad_order_schema" not in request_data:
            raise serializers.ValidationError("Bad formated json.")
        ad_order_schema = request_data["ad_order_schema"]
        if len(ad_order_schema) < 1:
            raise serializers.ValidationError("Bad formated json.")
        else:
            for key in ad_order_schema:
                get_object_or_404(Ad, id=ad_order_schema[key])

        return ad_order_schema

    def create(self, validated_data):
        ad_order_schema = self._cistom_order_schema_validator()

        program = super().create(validated_data)
        for key in ad_order_schema:
            ProgramAdMembership(ad=Ad.objects.get(id=ad_order_schema[key]),
                                program=program,
                                ad_index=int(key)).save()
        return program

    def update(self, instance, validated_data):
        ad_order_schema = self._cistom_order_schema_validator()

        program = super().update(instance, validated_data)
        program.ad_members.clear()
        for key in ad_order_schema:
            ProgramAdMembership(ad=Ad.objects.get(id=ad_order_schema[key]),
                                program=program,
                                ad_index=int(key)).save()
        return program


class ProgramAdMembershipSerializer(serializers.HyperlinkedModelSerializer):
    """Program ad memberships serializer"""

    class Meta:
        model = ProgramAdMembership
        fields = ("id", "url", "ad", "program",
                  "ad_index", "created_at", "updated_at")
        read_only_fields = ("ad", "program", "url")
