"""Models"""
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.db import models
from authentication.models import User
from pproviders.models import Pprovider
from daily_programs.models import DailyProgram
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

    daily_program = models.ForeignKey(
        DailyProgram,
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


@receiver(post_save, sender=Station)
def set_daily_program_in_use_on_save(sender, instance, **kwargs):
    if instance.daily_program:
        instance.daily_program.is_in_use = True
        instance.daily_program.save()


@receiver(pre_delete, sender=Station)
def set_daily_program_in_use_on_delete(sender, instance, **kwargs):
    if instance.daily_program:
        if len(Station.objects.filter(daily_program=instance.daily_program)) == 1:
            instance.daily_program.is_in_use = False
            instance.daily_program.save()
    return {
        "message": "Ok"
    }
