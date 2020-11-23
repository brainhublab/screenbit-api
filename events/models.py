"""Models"""
from django.db import models
from stations.models import Station
from ads.models import Ad
from django.utils.translation import ugettext as _
from settings import local_settings


class Event(models.Model):
    """
    Event Model
    """
    station = models.ForeignKey(
        Station,
        null=False,
        on_delete=models.PROTECT,
        related_name='Event')

    ad = models.ForeignKey(
        Ad,
        null=False,
        on_delete=models.CASCADE,
        related_name='Event')

    hour = models.CharField(
        max_length=2,
        choices=local_settings.HOURS,
        null=True,
        default="00")

    type = models.CharField(
        max_length=100,
        choices=local_settings.EVENTS,
        null=False,
        default=local_settings.VIEWER)

    button_clicks = models.IntegerField(null=True)
    # Duration will be stored as seconds
    duration = models.IntegerField(null=False,
                                   default=0)

    created_at = models.DateTimeField(auto_now_add=True)
