"""Models"""
from django.db import models
from authentication.models import User
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.fields import GenericRelation
from screenbit_core.models import File
from settings import local_settings
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator


class Ad(models.Model):
    """
    Advertising materials Model
    """
    creator = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='Ad')

    title = models.TextField(max_length=60, null=False, blank=False)
    description = models.TextField(max_length=300, null=False, blank=False)
    file = GenericRelation(File, null=False)

    VIDEO = "VD"
    IMAGE = "IM"
    GIF = "GF"
    MEDIA_TYPES = [
        (VIDEO, "Video media type"),
        (IMAGE, "Image media type"),
        (GIF, "GIF media type"),
    ]
    media_type = models.CharField(
        max_length=2,
        choices=MEDIA_TYPES,
        null=True)
    duration = models.FloatField(validators=[MaxValueValidator(1800)],
                                 null=True)
    desired_viewers = models.IntegerField(null=True)
    percent_to_load = models.IntegerField(validators=[MinValueValidator(1),
                                                      MaxValueValidator(100)],
                                          default=100)
    areas = ArrayField(
            models.CharField(choices=local_settings.AREAS, max_length=4, null=True),
            size=24, null=True)
    hours = ArrayField(
            models.CharField(choices=local_settings.HOURS, max_length=2, null=True),
            size=24, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
