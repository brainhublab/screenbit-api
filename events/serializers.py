from .models import Event
from stations.models import Station
from rest_framework import serializers
from settings import local_settings
from django.shortcuts import get_object_or_404
import jwt


class EventSerializer(serializers.HyperlinkedModelSerializer):
    """Advertising serializer"""

    token_secret = local_settings.SCREEN_TOKEN_SECRET

    class Meta:
        model = Event
        fields = ("id", "url", "station", "station_id", "ad", "ad_id",
                  "type", "hour", "duration", "button_clicks", "created_at", )
        read_only_fields = ("id", "url", "station", "created_at", )
        required_fields = ("duration", "ad", "type", "hour", )
        extra_kwargs = {field: {"required": True} for field in required_fields}

    def get_station_from_token(self):
        """Gets current user from request"""
        request = self.context.get("request")
        token = jwt.decode(request.META["HTTP_BIT_TOKEN"].split()[1],
                           self.token_secret)
        return get_object_or_404(Station, id=token["sub"])

    def validate(self, data):
        station = self.get_station_from_token()
        relations_exist = station.stadrelation.filter(ad=data["ad"], hour=data["hour"])
        if relations_exist:
            data["station"] = station
        else:
            raise serializers.ValidationError()
        if data["type"] == "btn_usr" and "button_clicks" not in data:
            raise serializers.ValidationError()
        return data
