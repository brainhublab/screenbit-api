from rest_framework import serializers
from .models import Ad

from screenbit_core.models import File
from screenbit_core.serializers import FileSerializer
from django.conf import settings


class AdSerializer(serializers.HyperlinkedModelSerializer):
    """Advertising serializer"""

    file = FileSerializer(
        many=True,
        read_only=True)

    class Meta:
        model = Ad
        fields = ("id", "url", "creator", "creator_id", "client", "client_id",
                  "title", "description", "file", "media_type",
                  "created_at", "updated_at")
        read_only_fields = ("id", "creator", "creator_id", "client_id",
                            "url", "created_at", "updated_at", "file", "media_type")
        required_fields = ("client" "title", "description")
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

    def create(self, validated_data):
        """ Add file objects while advertising object is on create"""
        """ Check count of image objects to create (allowed 1)"""
        media_file = self.context.get("view").request.FILES
        if len(media_file) != 1:
            raise serializers.ValidationError(
                ("You can update exactly one file!"))

        """ Check file extension """
        validated_data["media_type"] = is_ext_approved(media_file)
        ad_data = super().create(validated_data)
        for file in media_file.values():
            file = File.objects.create(content_object=ad_data, file=file)
        return ad_data

    def update(self, instance, validated_data):
        """ Replace file objects while Advertising object is on update"""
        """ Check count of image objects to create (allowed 1)"""
        media_file = self.context.get("view").request.FILES
        if len(media_file) != 1:
            raise serializers.ValidationError(
                ("You can update exactly one file!"))

        """ Check file extension """
        validated_data["media_type"] = is_ext_approved(media_file)
        ad_data = super().update(instance, validated_data)
        file_to_replace = File.objects.filter(object_id=instance.id)
        file_to_replace.delete()
        for file in media_file.values():
            file = File.objects.create(content_object=ad_data, file=file)
        return ad_data


def is_ext_approved(media_file):
    global_variable = settings.GLOBAL_VARIABLE
    if media_file["media_file"].name.split(".")[-1] in global_variable["approved_video_ext"]:
        return "VD"
    elif media_file["media_file"].name.split(".")[-1] in global_variable["approved_image_ext"]:
        return "IM"
    else:
        raise serializers.ValidationError({"message": "Unsupported file extension"})