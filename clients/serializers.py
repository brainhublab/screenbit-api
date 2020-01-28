from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    """Client serializer"""

    class Meta:
        model = Client
        fields = ("id", "url", "creator", "creator_id", "f_name", "l_name",
                  "organization", "email", "phone", "p_addr",
                  "created_at", "updated_at")

        read_only_fields = ("id", "creator", "creator_id", "url",
                            "created_at", "updated_at")

        required_fields = ("f_name", "l_name", "email", "phone", "p_addr")

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
