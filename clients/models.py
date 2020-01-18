"""Models"""
from django.db import models

from authentication.models import User
from django.utils.translation import ugettext as _


class Client(models.Model):
    """
    Client Model
    """
    creator = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='Client')

    f_name = models.TextField(max_length=60, null=False)
    l_name = models.TextField(max_length=60, null=False)
    organization = models.TextField(max_length=60, null=True)

    email = models.EmailField(('email address'), unique=True)
    phone = models.TextField(max_length=60, blank=False)
    p_addr = models.TextField(max_length=60, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return self.f_name + self.l_name
