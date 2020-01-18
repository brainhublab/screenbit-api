"""Models"""
from django.db import models
from authentication.models import User
from pproviders.models import Pprovider
from programs.models import Program
from django.utils.translation import ugettext as _


class Station(models.Model):
    """
    Station Model
    """
    creator = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='Station')

    pprovider = models.ForeignKey(
        Pprovider,
        null=True,
        on_delete=models.SET_NULL,
        related_name='Station')

    program = models.ForeignKey(
        Program,
        null=True,
        on_delete=models.SET_NULL,
        related_name='Station')

    title = models.TextField(max_length=60, blank=False)
    description = models.TextField(max_length=300, blank=False)

    """ List of cities to chose for location"""
    SOFIA = "SO"
    BURGAS = "BS"
    PLOVDIV = "PL"
    VARNA = "VA"
    CITIES = [
        (SOFIA, "Sofia city"),
        (BURGAS, "Burgas city"),
        (PLOVDIV, "Plovdiv city"),
        (VARNA, "Varna city"),
    ]
    city = models.CharField(
        max_length=2,
        choices=CITIES,
        null=True)

    mac_addr = models.TextField(max_length=300, blank=False, unique=True)
    net_addr = models.TextField(max_length=300, blank=True, unique=True)
    p_addr = models.TextField(max_length=300, blank=True)

    lat = models.DecimalField(max_digits=9,
                              decimal_places=7,
                              null=True)
    long = models.DecimalField(max_digits=10,
                               decimal_places=7,
                               null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
