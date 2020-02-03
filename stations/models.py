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

    TWELVE_AM = "00"
    ОNЕ_AM = "01"
    TWO_AM = "02"
    THREE_AM = "03"
    FOUR_AM = "04"
    FIVE_AM = "05"
    SIX_AM = "06"
    SEVEN_AM = "07"
    EIGHT_AM = "08"
    NINE_AM = "09"
    TEN_AM = "10"
    ELEVEN_AM = "11"
    TWELVE_PM = "12"
    ОНЕ_PM = "13"
    TWO_PM = "14"
    THREE_PM = "15"
    FOUR_PM = "16"
    FIVE_PM = "17"
    SIX_PM = "18"
    SEVEN_PM = "19"
    EIGHT_PM = "20"
    NINE_PM = "21"
    TEN_PM = "22"
    ELEVEN_PM = "23"
    HOURS = [
        (TWELVE_AM, "TWELVE AM"),
        (ОNЕ_AM, "ОNЕ AM"),
        (TWO_AM, "TWO AM"),
        (THREE_AM, "THREE AM"),
        (FOUR_AM, "FOUR AM"),
        (FIVE_AM, "FIVE AM"),
        (SIX_AM, "SIX AM"),
        (SEVEN_AM, "SEVEN AM"),
        (EIGHT_AM, "EIGHT AM"),
        (NINE_AM, "NINE AM"),
        (TEN_AM, "TEN AM"),
        (ELEVEN_AM, "ELEVEN AM"),
        (TWELVE_PM, "TWELVE PM"),
        (ОНЕ_PM, "ОНЕ PM"),
        (TWO_PM, "TWO PM"),
        (THREE_PM, "THREE PM"),
        (FOUR_PM, "FOUR PM"),
        (FIVE_PM, "FIVE PM"),
        (SIX_PM, "SIX PM"),
        (SEVEN_PM, "SEVEN PM"),
        (EIGHT_PM, "EIGHT PM"),
        (NINE_PM, "NINE PM"),
        (TEN_PM, "TEN PM"),
        (ELEVEN_PM, "ELEVEN PM")

    ]
    hour = models.CharField(
        max_length=2,
        choices=HOURS,
        null=True,
        default="00")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("station", "hour",)
