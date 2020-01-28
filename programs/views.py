from .models import Program
from .serializers import ProgramSerializer
from screenbit_core.permissions import IsAdminUserOrReadOnly
from rest_framework import viewsets, filters, serializers
from django_filters import rest_framework as django_rest_filters
from django.core.exceptions import PermissionDenied


class ProgramViewSet(viewsets.ModelViewSet):
    """
    Media program viewset
    """
    queryset = Program.objects.all()
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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        used_in = []
        daily_programs = instance.dailyprmembership.all()
        for related_daily in daily_programs:
            print(related_daily.daily_program.is_in_use)
            if related_daily.daily_program.is_in_use:
                used_in.append(related_daily.daily_program.id)
        print(used_in)
        if len(used_in) > 0:
            raise serializers.ValidationError({"message": "Ad is used in activ advertismen",
                                              "used_in": used_in})
        else:
            return super(ProgramViewSet, self).destroy(request, *args, **kwargs)
