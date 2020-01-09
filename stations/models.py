"""Models"""
from django.db import models
from django.contrib.postgres.fields import JSONField

from authentication.models import User
from place_providers.models import PlaceProvider
from django.utils.translation import ugettext as _


class Station(models.Model):
    """
    Station Model
    """
    creator = models.ForeignKey(
        User,
        null=False,
        on_delete=models.CASCADE,
        related_name='Station')

    place_provider = models.ForeignKey(
        PlaceProvider,
        null=True,
        on_delete=models.CASCADE,
        related_name='Station')

    name = models.TextField(max_length=60, blank=False)
    description = models.TextField(max_length=300, blank=False)

    mac_addr = models.TextField(max_length=300, blank=False, unique=True)
    net_addr = models.TextField(max_length=300, blank=False, unique=True)
    p_addr = models.TextField(max_length=300, blank=True)
    media_urls = JSONField(null=True)

    lat = models.DecimalField(max_digits=9,
                              decimal_places=7)
    long = models.DecimalField(max_digits=10,
                               decimal_places=7)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
