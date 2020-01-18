from .models import Ad
from .serializers import AdSerializer
from screenbit_core.permissions import IsAdminUserOrReadOnly

from rest_framework import viewsets, filters
from django.db.models import Q
from django_filters import rest_framework as django_rest_filters
from django.core.exceptions import PermissionDenied


class AdViewSet(viewsets.ModelViewSet):
    """
    Advertising viewset
    """
    queryset = Ad.objects.order_by('-created_at')
    serializer_class = AdSerializer
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_backends = (filters.SearchFilter,
                       django_rest_filters.DjangoFilterBackend, )
    search_fields = ["title", "description"]
    filterset_fields = ["creator_id", "client_id", "media_type"]

    def perform_create(self, serializer):
        """Add user that make request to serializer data"""
        if self.request.user:
            serializer.save(creator=self.request.user)
        else:
            raise PermissionDenied()
