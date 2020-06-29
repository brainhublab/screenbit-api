from .models import Event
from .serializers import EventSerializer
from .permissions import IsAuthenticatedScreen, IsAuthenticatedWorker
from rest_framework import viewsets, filters
from django.db.models import Q
from django_filters import rest_framework as django_rest_filters
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.decorators import action


class EventViewSet(viewsets.ModelViewSet):
    """
    Event viewset
    """
    queryset = Event.objects.order_by('-created_at')
    serializer_class = EventSerializer
    permission_classes = [HasAPIKey | IsAuthenticatedScreen]
    filter_backends = (filters.SearchFilter,
                       django_rest_filters.DjangoFilterBackend, )

    def filter_event_queryset(self, queryset, request):
        queryset = queryset.all()
        conditions = Q()

        ad_id = request.GET.get("ad_id")
        station_id = request.GET.get("station_id")
        type = request.GET.get('type')

        btn_clicks = request.GET.get('btn_clicks')
        gte_btn_clicks = request.GET.get('gte_btn_clicks')
        lte_btn_clicks = request.GET.get('lte_btn_clicks')

        hour = request.GET.get('hour')
        gte_hour = request.GET.get('gte_hour')
        lte_hour = request.GET.get('lte_hour')

        duration = request.GET.get('ex_duration')
        gte_duration = request.GET.get('gte_duration')
        lte_duration = request.GET.get('lte_duration')

        if ad_id:
            conditions.add(Q(ad_id=ad_id), Q.OR)
        if station_id:
            conditions.add(Q(station_id=station_id), Q.OR)
        if type:
            conditions.add(Q(type=type), Q.OR)

        if btn_clicks:
            conditions.add(Q(button_clicks=btn_clicks), Q.OR)
        else:
            if gte_btn_clicks:
                conditions.add(Q(button_clicks__gte=gte_btn_clicks), Q.AND)
            if lte_btn_clicks:
                conditions.add(Q(button_clicks__lte=lte_btn_clicks), Q.AND)

        if hour:
            conditions.add(Q(hour=hour), Q.OR)
        else:
            if gte_hour:
                conditions.add(Q(hour__gte=gte_hour), Q.AND)
            if lte_hour:
                conditions.add(Q(hour__lte=lte_hour), Q.AND)

        if duration:
            conditions.add(Q(duration=duration), Q.OR)
        else:
            if gte_duration:
                conditions.add(Q(duration__gte=gte_duration), Q.AND)
            if lte_duration:
                conditions.add(Q(duration__lte=lte_duration), Q.AND)

        return queryset.filter(conditions)

    def list(self, request):
        self.queryset = self.filter_event_queryset(self.queryset, request)
        serializer = self.serializer_class(self.queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, permission_classes=[IsAuthenticatedWorker], methods=['get'])
    def tasks(self, request):
        data = request.data
        # TODO: complete the request
        print(data)
        return Response({"message": "Work!"}, 200)
