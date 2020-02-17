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

    def filter_feedbacks_queryset(self, queryset, request):
        queryset = queryset.all()
        conditions = Q()

        ad_id = request.GET.get("ad_id")
        if ad_id:
            conditions.add(Q(ad_id=ad_id), Q.OR)

        min_duration = request.GET.get("min_duration")
        max_duration = request.GET.get("max_duration")
        if min_duration and min_duration:
            conditions.add(Q(duration__range=(min_duration, max_duration)), Q.OR)
        else:
            gte_duration = request.GET.get('gte_duration')
            if gte_duration:
                conditions.add(Q(duration__gte=gte_duration), Q.OR)

            lte_duration = request.GET.get('lte_duration')
            if lte_duration:
                conditions.add(Q(duration__lte=lte_duration), Q.OR)

            ex_duration = request.GET.get('ex_duration')
            if ex_duration:
                conditions.add(Q(duration=ex_duration), Q.OR)

        return queryset.filter(conditions)

    def list(self, request):
        self.queryset = self.filter_feedbacks_queryset(self.queryset, request)
        serializer = self.serializer_class(self.queryset, many=True, context={'request': request})
        return Response(serializer.data)
