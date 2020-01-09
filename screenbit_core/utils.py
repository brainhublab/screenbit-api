
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer

from django.urls import resolve

# from notifications.models import Notification
from django.core.cache import cache

from django.utils.translation import ugettext as _

def fix_django_headers(meta):
    """
    Fix this nonsensical API:
    https://docs.djangoproject.com/en/1.11/ref/request-response/
    https://code.djangoproject.com/ticket/20147
    """
    ret = {}
    for k, v in meta.items():
        if k.startswith("HTTP_"):
            k = k[len("HTTP_"):]
        elif k not in ("CONTENT_LENGTH", "CONTENT_TYPE"):
            # Skip CGI garbage
            continue
        ret[k.lower().replace("_", "-")] = v
    return ret
