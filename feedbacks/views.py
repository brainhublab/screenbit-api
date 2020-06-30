from .models import Feedback
from .serializers import FeedbackSerializer
from .permissions import IsAdminUser, IsAdminUserOrOwner, IsAuthenticatedWorker
from rest_framework import viewsets, filters
from django.db.models import Q, F
from django_filters import rest_framework as django_rest_filters
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.decorators import action
from stations.models import Station
from ads.models import Ad


class FeedbackViewSet(viewsets.ModelViewSet):
    """
    Feedback viewset
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [HasAPIKey | IsAdminUserOrOwner]
    filter_backends = (filters.SearchFilter,
                       django_rest_filters.DjangoFilterBackend, )

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAdminUserOrOwner]
        else:
            permission_classes = [IsAdminUser | IsAuthenticatedWorker]
        return [permission() for permission in permission_classes]

    def filter_feedback_queryset(self, queryset, request):
        queryset = queryset.all()
        conditions = Q()

        ad_id = request.GET.get("ad__id")
        station_id = request.GET.get("station__id")

        if ad_id:
            conditions.add(Q(ad_id=ad_id), Q.OR)
        if station_id:
            conditions.add(Q(station_id=station_id), Q.OR)

        return queryset.filter(conditions)

    def list(self, request):
        if hasattr(request, "user"):
            if request.user.is_admin:
                self.queryset = self.filter_feedback_queryset(self.queryset, request)
            else:
                self.queryset = self.filter_feedback_queryset(self.queryset.filter(ad__creator=request.user), request)
        else:
            return False
        serializer = self.serializer_class(self.queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, permission_classes=[IsAuthenticatedWorker], methods=['post'])
    def worker(self, request):
        """ create or update feedback data (worker) """
        data = request.data
        ad = Ad.objects.filter(pk=data["ad_id"]).first()
        station = Station.objects.filter(pk=data["station_id"]).first()
        feed = Feedback.objects.filter(station=station,
                                       ad=ad,
                                       hour=data["hour"]).update(viewers=F("viewers") + data["viewers"],
                                                                 holders=F("holders") + data["holders"],
                                                                 button_usrs=F("button_usrs") + data["button_usrs"],
                                                                 reached=F("reached") + data["reached"])
        if feed:
            return Response()
        else:
            Feedback.objects.create(station=station,
                                    ad=ad,
                                    hour=data["hour"],
                                    area=station.area,
                                    viewers=data["viewers"],
                                    holders=data["holders"],
                                    button_usrs=data["button_usrs"],
                                    reached=data["reached"])
            return Response()
