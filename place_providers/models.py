"""Models"""
from django.db import models

from authentication.models import User
from django.utils.translation import ugettext as _


class PlaceProvider(models.Model):
    """
    Place provider Model
    """
    creator = models.ForeignKey(
        User,
        null=False,
        on_delete=models.CASCADE,
        related_name='PlaceProvider')

    f_name = models.TextField(max_length=60, blank=False)
    l_name = models.TextField(max_length=60, blank=False)
    organization = models.TextField(max_length=60, blank=True)

    email = models.EmailField(('email address'), unique=True)
    phone = models.TextField(max_length=60, blank=False)
    p_addr = models.TextField(max_length=60, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
