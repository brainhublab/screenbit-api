from .models import Event
from .serializers import EventSerializer
from .permissions import IsAuthenticatedScreen
from rest_framework import viewsets, filters
from django.db.models import Q
from django_filters import rest_framework as django_rest_filters
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey


class EventViewSet(viewsets.ModelViewSet):
    """
    Event viewset
    """
    queryset = Event.objects.order_by('-created_at')
    serializer_class = EventSerializer
    permission_classes = [HasAPIKey | IsAuthenticatedScreen]
    filter_backends = (filters.SearchFilter,
                       django_rest_filters.DjangoFilterBackend, )
