from .models import Station
from programs.models import ProgramAdMembership
from .serializers import StationSerializer, StationLocationSerializer
from screenbit_core.permissions import IsAdminUserOrReadOnly
from settings.local_settings import MEDIA_URL

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, filters, serializers

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django_filters import rest_framework as django_rest_filters


class StationViewSet(viewsets.ModelViewSet):
    """
    Station Viewset
    """
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_backends = (filters.SearchFilter,
                       django_rest_filters.DjangoFilterBackend, )
    search_fields = ["title", "city", "pprovider"]
    filterset_fields = ["creator_id", "city", "pprovider", "mac_addr"]

    def perform_create(self, serializer):
        """Add user that make request to serializer data"""
        if self.request.user:
            serializer.save(creator=self.request.user)
        else:
            raise PermissionDenied()

    def filter_statoins_queryset(self, queryset, request):
        """Filter stations by title or citi or place provider"""
        query = request.GET.get('search')
        query = request.GET.get('title')
        query = request.GET.get('citi')
        queryset = queryset.all()
        condition = Q()

        if query:
            q_condition = Q()
            q_condition.add(Q(title__icontains=query), Q.OR)
            q_condition.add(Q(title__icontains=query), Q.OR)
            q_condition.add(Q(citi__icontains=query), Q.OR)
            condition.add(q_condition, Q.AND)
        return queryset.filter(condition).distinct()

    @action(detail=False, methods=['get'])
    def free_stations(self, request):
        """ Function for filtering stations that are free for hours list """
        if "hours" not in request.data:
            return Response({"message": "Bad request"}, 400)
        global_variables = settings.GLOBAL_VARIABLE
        available_ext = all(elem in global_variables[0]["available_hours_choices"] for elem in request.data["hours"])
        if available_ext:
            busy_stations = Station.objects.filter(stprrelation__hour__in=request.data["hours"])
            free_stations = Station.objects.exclude(id__in=busy_stations)

            serializer = self.serializer_class(
                instance=free_stations, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({"message": "Bad Request"}, 400)

    @action(detail=False, methods=['get'])
    def media(self, request):
        params = self.request.query_params
        if "mac_addr" in params:
            mac_addr = int(params["mac_addr"])
            station = get_object_or_404(Station, mac_addr=mac_addr)
        elif "id" in params:
            id = int(params["id"])
            station = get_object_or_404(Station, id=id)
        else:
            raise serializers.ValidationError({"message": "Missing parameter"})

        if station.programs is not None:
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


def station_portal_view(request):
    return render(request, 'templates/index.html')
