import binascii
import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from stations.models import Station

from django.db.models.signals import post_save
from django.dispatch import receiver


class StationToken(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)

    station = models.OneToOneField(
        Station, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name="Station"
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(StationToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key


@receiver(post_save, sender=Station)
def on_station_created(sender, instance, created, **kwargs):
    """ Create authentication token for Station obj """
    if created:
        station_token = StationToken.objects.create(
            station=instance
        )
        station_token.save()
