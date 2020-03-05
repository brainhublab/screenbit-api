"""Models"""
from django.db import models
from stations.models import Station
from ads.models import Ad
from django.utils.translation import ugettext as _


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

    """ Duration will be stored as seconds """
    duration = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
