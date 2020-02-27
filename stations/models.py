"""Models"""
from django.db import models
from authentication.models import User
from programs.models import Program
from django.utils.translation import ugettext as _
from settings import local_settings


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
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='StationPlaceProvider')

    programs = models.ManyToManyField(Program, through="StationProgramRelation")

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

    area = models.CharField(
        max_length=4,
        choices=local_settings.AREAS,
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


class StationProgramRelation(models.Model):

    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='stprrelation')
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='stprrelation')

    hour = models.CharField(
        max_length=2,
        choices=local_settings.HOURS,
        null=True,
        default="00")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("station", "hour",)
