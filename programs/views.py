from .models import Program
from .serializers import ProgramSerializer
from screenbit_core.permissions import IsAdminUserOrReadOnly

from rest_framework import viewsets, filters
from django_filters import BaseInFilter, CharFilter, rest_framework as django_rest_filters

from django.core.exceptions import PermissionDenied

# """ Custom filter to find media programs which
#     contain specific advertising """
#
#
# class CharInFilter(BaseInFilter, CharFilter):
#     pass
#
#
# class IdsArrFilter(django_rest_filters.FilterSet):
#     ad_ids = CharInFilter(field_name='ad_ids', lookup_expr='contains')
#     media_urls = CharInFilter(field_name='media_urls', lookup_expr='contains')
#
#     class Meta:
#         model = Program
#         fields = (
#             "ad_ids",
#             # "media_urls"
#         )


class ProgramViewSet(viewsets.ModelViewSet):
    """
    Media program viewset
    """
    queryset = Program.objects.order_by('-created_at')
    serializer_class = ProgramSerializer
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
