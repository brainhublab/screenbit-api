from .models import Feedback
from .serializers import FeedbackSerializer
from .permissions import IsAdminUserOrOwner, IsAuthenticatedWorker
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
    permission_classes = [HasAPIKey | IsAdminUserOrOwner]
    filter_backends = (filters.SearchFilter,
                       django_rest_filters.DjangoFilterBackend, )

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAdminUserOrOwner | IsAuthenticatedWorker]
        else:
            permission_classes = [IsAuthenticatedWorker]
        return [permission() for permission in permission_classes]

    def filter_feedback_queryset(self, queryset, request):
        queryset = queryset.all()
        conditions = Q()

        ad_id = request.GET.get("ad_id")
        station_id = request.GET.get("station_id")

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
