"""Models"""
from django.db import models
from stations.models import Station
from ads.models import Ad
from django.utils.translation import ugettext as _
from settings import local_settings


class Feedback(models.Model):
    """
    Feedback Model
    """
    station = models.ForeignKey(
        Station,
        null=False,
        on_delete=models.CASCADE,
        related_name='Feedback')

    ad = models.ForeignKey(
        Ad,
        null=False,
        on_delete=models.CASCADE,
        related_name='Feedback')

    area = models.CharField(
        max_length=4,
        choices=local_settings.AREAS,
        null=True)

    hour = models.CharField(
        max_length=4,
        choices=local_settings.HOURS,
        null=True)

    viewers = models.IntegerField(default=0)
    holders = models.IntegerField(default=0)
    button_usrs = models.IntegerField(default=0)
    reached = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
