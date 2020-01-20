from rest_framework import serializers

from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_text

from .models import Image, File


class CreatableSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get_or_create(**{self.slug_field: data})[0]
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field,
                      value=smart_text(data))
        except (TypeError, ValueError):
            self.fail('invalid')


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    """
    Image serializer
    """
    class Meta:
        model = Image
        fields = ('id', 'url', 'image', )
        read_only_fields = fields


class FileSerializer(serializers.HyperlinkedModelSerializer):
    """
    File serializer
    """
    class Meta:
        model = File
        fields = ('id', 'url', 'file', "created_at", "updated_at", )
        read_only_fields = ('id', 'url', 'file', "created_at", "updated_at",)
