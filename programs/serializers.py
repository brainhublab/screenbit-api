from rest_framework import serializers
from .models import Program
from ads.models import Ad
from ads.serializers import AdSerializer
from django.shortcuts import get_object_or_404


class ProgramSerializer(serializers.HyperlinkedModelSerializer):
    """Media Program serializer"""

    class Meta:
        model = Program
        fields = ("id", "url", "creator", "creator_id", "title", "description",
                  "ads", "created_at", "updated_at")
        read_only_fields = ("id", "url", "creator", "creator_id",
                            "created_at", "updated_at")
        required_fields = ("client", "ads", "title", "description")
        unique_together = ['ads', 'program', 'order']
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
