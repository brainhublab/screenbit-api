from .models import Ad
from .serializers import AdSerializer
from .permissions import IsAdminUserOrOwner
from rest_framework import viewsets, filters, serializers
from django.db.models import Q
from django_filters import rest_framework as django_rest_filters
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response

from rest_framework_api_key.permissions import HasAPIKey


class AdViewSet(viewsets.ModelViewSet):
    """
    Advertising viewset
    """
    queryset = Ad.objects.order_by('-created_at')
    serializer_class = AdSerializer
    permission_classes = [HasAPIKey | IsAdminUserOrOwner]
    filter_backends = (filters.SearchFilter,
                       django_rest_filters.DjangoFilterBackend, )

    def perform_create(self, serializer):
        """Add user that make request to serializer data"""
        if self.request.user:
            serializer.save(creator=self.request.user)
        else:
            raise PermissionDenied()

    def filter_ads_queryset(self, queryset, request):
        queryset = queryset.all()
        conditions = Q()

        if request.user.is_admin:
            creator_id = request.GET.get("creator_id")
            if creator_id:
                conditions.add(Q(creator_id=creator_id), Q.OR)

        title = request.GET.get('title')
        if title:
            conditions.add(Q(title__icontains=title), Q.OR)

        description = request.GET.get('description')
        if description:
            conditions.add(Q(description__icontains=description), Q.OR)

        media_type = request.GET.get("media_type")
        if media_type:
            conditions.add(Q(media_type=media_type), Q.OR)

        return queryset.filter(conditions)

    def list(self, request):
        if not request.user.is_admin and not request.user.is_staff:
            self.queryset = self.queryset.filter(creator=request.user)

        self.queryset = self.filter_ads_queryset(self.queryset, request)
        serializer = self.serializer_class(self.queryset, many=True, context={'request': request})
        return Response(serializer.data)

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
