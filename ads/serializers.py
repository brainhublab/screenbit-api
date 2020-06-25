from rest_framework import serializers
from .models import Ad
from screenbit_core.models import File
from screenbit_core.serializers import FileSerializer
from django.conf import settings
from .utils import ad_media_disable, ad_media_loader
from moviepy.editor import VideoFileClip
global_variables = settings.GLOBAL_VARIABLE[0]


class AdSerializer(serializers.HyperlinkedModelSerializer):
    """Advertising serializer"""

    file = FileSerializer(
        many=True,
        read_only=True)

    class Meta:
        model = Ad
        fields = ("id", "url", "creator", "creator_id", "desired_viewers", "percent_to_load",
                  "title", "description", "file", "media_type", "areas", "hours",
                  "is_active", "duration", "created_at", "updated_at")
        read_only_fields = ("id", "creator", "creator_id",
                            "url", "is_active", "created_at", "updated_at", "file", "media_type")
        required_fields = ("title", "description", "areas", "hours", "duration" "desired_viewers", "percent_to_load")
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

    def validate_duration(self, value):
        if value is not None:
            if value > 0:
                return value
            else:
                raise serializers.ValidationError(
                    ("Duration valuie must be bigger than 0"))

    def create(self, validated_data):
        """ Add file objects while advertising object is on create"""
        """ Check count of image objects to create (allowed 1)"""
        media_file = self.context.get("view").request.FILES
        if len(media_file) != 1:
            raise serializers.ValidationError(
                ("You can update exactly one file!"))

        """ Check file extension """
        file_ext = is_ext_approved(media_file)
        validated_data["media_type"] = file_ext

        """ Save new file and duration value """
        for file in media_file.values():
            if file_ext == "VD":
                """ load file information (if video) to get duration """
                file_info = VideoFileClip(file.temporary_file_path())
                validated_data["duration"] = file_info.duration
            elif "duration" not in validated_data:
                raise serializers.ValidationError(
                    ({"duration": "Missing duration value!"}))
            ad_data = super().create(validated_data)
            file = File.objects.create(content_object=ad_data, file=file)
        """ Load new media to screens """
        ad_media_loader(ad_data)
        return ad_data

    def update(self, instance, validated_data):
        """ Replace file objects while Advertising object is on update"""
        """ Check count of image objects to create (allowed 1)"""
        media_file = self.context.get("view").request.FILES
        if len(media_file) != 1:
            raise serializers.ValidationError(
                ("You can update exactly one file!"))

        """ Check file extension """
        file_ext = is_ext_approved(media_file)
        validated_data["media_type"] = file_ext
        """ Disable old media from screens """
        ad_media_disable(instance)

        """ Delete old file from DB """
        file_to_replace = File.objects.filter(object_id=instance.id)
        file_to_replace.delete()

        """ Save new file and duration value """
        for file in media_file.values():
            if file_ext == "VD":
                """ load file information (if video) to get duration """
                file_info = VideoFileClip(file.temporary_file_path())
                validated_data["duration"] = file_info.duration
            elif "duration" not in validated_data:
                raise serializers.ValidationError(
                    ({"duration": "Missing duration value!"}))
            ad_data = super().update(instance, validated_data)
            file = File.objects.create(content_object=ad_data, file=file)
        """ Load new media to screens """
        ad_media_loader(ad_data)
        return ad_data


def is_ext_approved(media_file):
    global_variables = settings.GLOBAL_VARIABLE
    if media_file["media_file"].name.split(".")[-1] in global_variables[0]["approved_video_ext"]:
        return "VD"
    elif media_file["media_file"].name.split(".")[-1] in global_variables[0]["approved_image_ext"]:
        return "IM"
    else:
        raise serializers.ValidationError({"message": "Unsupported file extension"})


class ActiveAdsIdsSerializer(serializers.ModelSerializer):
    """ Active advertisments id's
        Used tp return only id's"""
    class Meta:
        model = Ad
        fields = ("id", )
        read_only_fields = fields
