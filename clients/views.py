from .models import Client
from .serializers import ClientSerializer
from screenbit_core.permissions import IsAdminUserOrReadOnly

from rest_framework import viewsets, filters
from django.db.models import Q
from django_filters import rest_framework as django_rest_filters
from django.core.exceptions import PermissionDenied


class ClientViewSet(viewsets.ModelViewSet):
    """
    Client viewset
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_backends = (filters.SearchFilter,
                       django_rest_filters.DjangoFilterBackend, )
    search_fields = ["email", "phone", "p_addr",
                     "f_name", "l_name", "organization"]
    filterset_fields = ["creator_id"]

    def perform_create(self, serializer):
        """Add user that make request to serializer data"""
        if self.request.user:
            serializer.save(creator=self.request.user)
        else:
            raise PermissionDenied()
