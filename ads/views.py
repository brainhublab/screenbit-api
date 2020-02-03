from .models import Ad
from .serializers import AdSerializer
from screenbit_core.permissions import IsAdminUserOrReadOnly

from rest_framework import viewsets, filters, serializers
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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        used_in = []
        for related_program in instance.program_set.all():
            ProgramStationRelations = related_program.stprrelation.all()
            for relation in ProgramStationRelations:
                relation_info = {
                    "program": relation.program,
                    "station": relation.station
                }
                used_in.append(relation_info)
        if len(used_in) > 0:
            raise serializers.ValidationError({"message": "Ad is used in activ advertismen",
                                               "used_in": used_in})
        else:
            return super(AdViewSet, self).destroy(request, *args, **kwargs)
