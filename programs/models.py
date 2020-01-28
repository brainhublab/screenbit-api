"""Models"""
from django.db import models
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

    ad_members = models.ManyToManyField(Ad, through='ProgramAdMembership')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProgramAdMembership(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='pradmembership')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='pradmembership')
    ad_index = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
