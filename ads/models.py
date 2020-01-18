"""Models"""
from django.db import models

from authentication.models import User
from clients.models import Client
from django.utils.translation import ugettext as _

from django.contrib.contenttypes.fields import GenericRelation
from screenbit_core.models import File


class Ad(models.Model):
    """
    Advertising materials Model
    """
    creator = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='Ad')

    client = models.ForeignKey(
        Client,
        null=True,
        on_delete=models.CASCADE,
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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
