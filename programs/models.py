"""Models"""
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from ads.models import Ad
from authentication.models import User
from django.utils.translation import ugettext as _


class Program(models.Model):
    """
    Media program Model
    """
    creator = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='Program')

    title = models.TextField(max_length=60, null=False, blank=False)
    description = models.TextField(max_length=300, null=False, blank=False)

    ads = models.ManyToManyField(Ad)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
