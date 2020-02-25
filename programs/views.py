from .models import Program
from .serializers import ProgramSerializer
from .permissions import IsAdminUser
from rest_framework.response import Response

from rest_framework import viewsets, filters, serializers
from django.db.models import Q
from django_filters import rest_framework as django_rest_filters
from django.core.exceptions import PermissionDenied
from rest_framework_api_key.permissions import HasAPIKey


class ProgramViewSet(viewsets.ModelViewSet):
    """
    Media program viewset
    """
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [HasAPIKey | IsAdminUser]

    filter_backends = (filters.SearchFilter,
                       django_rest_filters.DjangoFilterBackend, )

    def perform_create(self, serializer):
        """Add user that make request to serializer data"""
        if self.request.user:
            serializer.save(creator=self.request.user)
        else:
            raise PermissionDenied()

    def filter_program_queryset(self, queryset, request):
        queryset = queryset.all()

        ad_conditions = Q()
        ad_id = request.GET.get("ad_id")
        if ad_id:
            ad_conditions.add(Q(pradmembership__ad_id=ad_id), Q.OR)
            queryset = queryset.filter(ad_conditions)

        conditions = Q()
        title = request.GET.get('title')
        if title:
            conditions.add(Q(title__contains=title), Q.OR)

        description = request.GET.get('description')
        if description:
            conditions.add(Q(description__contains=description), Q.OR)

        creator_id = request.GET.get("creator_id")
        if creator_id:
            creator_id.add(Q(creator_id=creator_id), Q.OR)

        return queryset.filter(conditions)

    def list(self, request):
        programs = self.filter_program_queryset(self.queryset, request)
        serializer = self.serializer_class(
                    programs, many=True, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        used_in = []
        ProgramStationRelations = instance.stprrelation.all()
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
            return super(ProgramViewSet, self).destroy(request, *args, **kwargs)
