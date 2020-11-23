import jwt
from datetime import datetime, timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _
from stations.models import Station

from django.db.models.signals import post_save
from django.dispatch import receiver
from settings import local_settings


class StationToken(models.Model):
    """
    The default authorization token model.
    """
    token = models.CharField(_("Token"), max_length=250, primary_key=True)

    station = models.OneToOneField(
        Station, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name="Station"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.create_token(self.station)
        return super(StationToken, self).save(*args, **kwargs)

    def create_token(self, station):
        payload = {
            'sub': station.id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=1825)  # 5 years
        }
        token = jwt.encode(payload, local_settings.SCREEN_TOKEN_SECRET)
        return token.decode('unicode_escape')

    def __str__(self):
        return self.token


@receiver(post_save, sender=Station)
def on_station_created(sender, instance, created, **kwargs):
    """Create authentication token for Station obj"""
    if created:
        station_token = StationToken.objects.create(
            station=instance
        )
        station_token.save()
