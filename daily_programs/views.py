from .models import DailyProgram
from .serializers import DailyProgramSerializer
from screenbit_core.permissions import IsAdminUserOrReadOnly

from rest_framework import viewsets, filters
from django_filters import rest_framework as django_rest_filters

from django.core.exceptions import PermissionDenied


class DailyProgramViewSet(viewsets.ModelViewSet):
    """
    DaiMedia program viewset
    """
    queryset = DailyProgram.objects.order_by('-created_at')
    serializer_class = DailyProgramSerializer
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_backends = (filters.SearchFilter,
                       django_rest_filters.DjangoFilterBackend, )

    search_fields = ["title", "description"]

    def perform_create(self, serializer):
        """Add user that make request to serializer data"""
        if self.request.user:
            serializer.save(creator=self.request.user)
        else:
            raise PermissionDenied()
        print(serializer.data)
