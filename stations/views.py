from .models import Station
from programs.models import ProgramAdMembership
from .serializers import StationSerializer, StationLocationSerializer

from .permissions import IsAdminUser, IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from settings.local_settings import MEDIA_URL
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, filters, serializers

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.db.models import Sum
from django.core.exceptions import PermissionDenied
from django_filters import rest_framework as django_rest_filters

global_variables = settings.GLOBAL_VARIABLE[0]


class StationViewSet(viewsets.ModelViewSet):
    """
    Station Viewset
    """
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = [HasAPIKey | IsAdminUser]
    filter_backends = (filters.SearchFilter,
                       django_rest_filters.DjangoFilterBackend, )

    def perform_create(self, serializer):
        """Add user that make request to serializer data"""
        if self.request.user:
            serializer.save(creator=self.request.user)
        else:
            raise PermissionDenied()

    def filter_statoins_queryset(self, queryset, request):
        """Filter stations by by free hours, title, city"""

        queryset = queryset.all()
        hours_condition = Q()
        if "free_hours" in request.data:
            hours_condition.add(Q(stprrelation__hour__in=request.data["free_hours"]), Q.AND)
            queryset = queryset.exclude(hours_condition)

        elif "busy_hours" in request.data:
            hours_condition.add(Q(stprrelation__hour__in=request.data["busy_hours"]), Q.AND)
            queryset = queryset.filter(hours_condition)

        another_conditions = Q()

        title = request.GET.get('title')
        if title:
            another_conditions.add(Q(title__icontains=title), Q.OR)

        description = request.GET.get('description')
        if description:
            another_conditions.add(Q(description__icontains=description), Q.OR)

        city = request.GET.get('city')
        if city:
            another_conditions.add(Q(city__icontains=city), Q.OR)

        mac_addr = request.GET.get('mac_addr')
        if mac_addr:
            another_conditions.add(Q(mac_addr__icontains=mac_addr), Q.OR)

        net_addr = request.GET.get('net_addr')
        if net_addr:
            another_conditions.add(Q(net_addr__icontains=net_addr), Q.OR)

        p_addr = request.GET.get('p_addr')
        if p_addr:
            another_conditions.add(Q(p_addr__icontains=p_addr), Q.OR)

        return queryset.filter(another_conditions)

    def list(self, request):
        """Custom list processing"""
        hours_data = []
        if "free_hours" in request.data:
            hours_data = request.data["free_hours"]
        elif "busy_hours" in request.data:
            hours_data = request.data["busy_hours"]

        if not all(elem in global_variables["available_hours_choices"] for elem in hours_data):
            return Response({"message": "Bad Request"}, 400)

        stations = self.filter_statoins_queryset(self.queryset, request)
        serializer = self.serializer_class(stations, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, permission_classes=[], methods=['get'])
    def media(self, request):
        params = self.request.query_params
        if "mac_addr" in params:
            mac_addr = params["mac_addr"]
            station = get_object_or_404(Station, mac_addr=mac_addr)
        elif "id" in params:
            """ Get program by id for development """
            id = int(params["id"])
            station = get_object_or_404(Station, id=id)
        else:
            raise serializers.ValidationError({"message": "Missing parameter"})

        if station.programs is not None:
            if "hour" in params:
                if params["hour"] not in global_variables["available_hours_choices"]:
                    return Response({"message": "Bad Request"}, 409)
                related_programs = station.stprrelation.filter(hour=params["hour"])
            else:
                related_programs = station.stprrelation.all().order_by("-hour")
            media_data = {}
            for relation in related_programs:
                media_data[relation.hour] = {}
                media_data[relation.hour]["program_id"] = relation.program.id
                program_ad_members = ProgramAdMembership.objects.filter(program=relation.program).order_by("ad_index")
                media_data[relation.hour]["program_data"] = {}
                for program_ad_member in program_ad_members:
                    media_data[relation.hour]["program_data"][program_ad_member.ad_index] = {"type":
                                                                                             program_ad_member.ad.media_type,
                                                                                             "url":
                                                                                             MEDIA_URL + str(program_ad_member.ad.file.get().file)
                                                                                             }
            return Response(media_data)
        else:
            return Response({
                "message": "This station dont have media program."
                })

    @action(detail=False, methods=['get'])
    def locations(self, request):
        """Action that return only stations locations data"""
        if self.request.user:
            """Get stations by title or citi or place provider"""
            queryset = self.filter_companies_queryset(self.queryset, request)
            """Search by latitude, longitude and distance / optional /"""
            params = self.request.query_params
            if "lat1" in params and "long1" in params and "lat2" in params and "long2" in params:
                lat1 = float(params["lat1"])
                lat2 = float(params["lat2"])
                long1 = float(params["long1"])
                long2 = float(params["long2"])

                obj_in_distance = queryset.filter(lat__lte=lat1, lat__gte=lat2,
                                                  long__gte=long1, long__lte=long2)
                serializer = StationLocationSerializer(
                    instance=obj_in_distance, many=True, context={'request': request})
                return Response(serializer.data)
            else:
                serializer = StationLocationSerializer(
                    instance=queryset, many=True, context={'request': request})
                return Response(serializer.data)
        else:
            raise serializer.ValidationError(("Login please"))

    @action(detail=False, permission_classes=[HasAPIKey | IsAuthenticated], methods=['get'], url_path='areas/viewers')
    def viewers(self, request):
        """ Return count of all potential screen viewers in current area """
        if "areas" in request.GET:
            potential_viewwers = Station.objects.filter(area__in=request.GET.getlist("areas")).aggregate(Sum("viewers"))
            return Response(potential_viewwers, 200)
        else:
            return Response({"message": "Bad request parameters"}, 400)


def station_portal_view(request):
    return render(request, 'templates/index.html')
