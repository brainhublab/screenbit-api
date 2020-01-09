"""Models"""
from django.db import models

from authentication.models import User
from django.utils.translation import ugettext as _


class Feedback(models.Model):
    """
    Feedback Model
    """
    creator = models.ForeignKey(
        User,
        null=False,
        on_delete=models.CASCADE,
        related_name='Feedback')

    ad = models.ForeignKey(
        User,
        null=False,
        on_delete=models.CASCADE,
        related_name='Feedback')

    qr_users = models.Integer()
    viewers = models.Integer()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
