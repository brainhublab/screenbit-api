from .models import Feedback
from stations.models import Station
from rest_framework import serializers
from station_auth.models import StationToken


class FeedbackSerializer(serializers.HyperlinkedModelSerializer):
    """Advertising serializer"""

    class Meta:
        model = Feedback
        fields = ("id", "url", "station", "station_id", "program", "program_id",
                  "ad", "ad_id", "duration", "created_at", "updated_at")
        read_only_fields = ("id", "url", "station", "program_id", "ad_id",
                            "created_at", "updated_at")
        required_fields = ("duration", "program", "ad",)
        extra_kwargs = {field: {"required": True} for field in required_fields}

    def get_station_from_token(self):
        """Gets current user from request"""
        request = self.context.get("request")
        token = request.META["HTTP_BIT_TOKEN"].split()[1]
        token_obj = StationToken.objects.filter(key=token).first()
        if token_obj:
            return token_obj.station
        return None

    def validate(self, data):
        station = self.get_station_from_token()
        if station:
            relations_exist = Station.objects.filter(id=station.id,
                                                     stprrelation__program=data["program"],
                                                     stprrelation__program__pradmembership__ad=data["ad"]).first()

            if relations_exist:
                data["station"] = station
                return data
            else:
                raise serializers.ValidationError()
        else:
            raise serializers.ValidationError()
