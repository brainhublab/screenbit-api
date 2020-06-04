from .models import Feedback
from .serializers import FeedbackSerializer
from .permissions import IsAuthenticatedScreen
from rest_framework import viewsets, filters
from django.db.models import Q
from django_filters import rest_framework as django_rest_filters
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey


class FeedbackViewSet(viewsets.ModelViewSet):
    """
    Feedback viewset
    """
    queryset = Feedback.objects.order_by('-created_at')
    serializer_class = FeedbackSerializer
    permission_classes = [HasAPIKey | IsAuthenticatedScreen]
    filter_backends = (filters.SearchFilter,
                       django_rest_filters.DjangoFilterBackend, )

    def filter_feedback_queryset(self, queryset, request):
        queryset = queryset.all()
        conditions = Q()

        ad_id = request.GET.get("ad_id")
        station_id = request.GET.get("station_id")
        ex_duration = request.GET.get('ex_duration')
        gte_duration = request.GET.get('gte_duration')
        lte_duration = request.GET.get('lte_duration')

        if ad_id:
            conditions.add(Q(ad_id=ad_id), Q.OR)
        if station_id:
            conditions.add(Q(station_id=station_id), Q.OR)
        if ex_duration:
            conditions.add(Q(duration=ex_duration), Q.OR)
        else:
            if gte_duration:
                conditions.add(Q(duration__gte=gte_duration), Q.AND)
            if lte_duration:
                conditions.add(Q(duration__lte=lte_duration), Q.AND)
        return queryset.filter(conditions)

    def list(self, request):
        self.queryset = self.filter_feedback_queryset(self.queryset, request)
        serializer = self.serializer_class(self.queryset, many=True, context={'request': request})
        return Response(serializer.data)
