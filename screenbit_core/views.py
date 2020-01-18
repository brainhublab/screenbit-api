from rest_framework import viewsets
from django_filters import rest_framework as django_rest_filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Image, File
from .permissions import IsOwnerOrReadOnly
from .serializers import ImageSerializer, FileSerializer


class ImageViewSet(viewsets.ModelViewSet):
    """
    Image viewset
    """
    queryset = Image.objects.order_by("-created_at")
    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )

    filter_backends = (django_rest_filters.DjangoFilterBackend, )


class FileViewSet(viewsets.ModelViewSet):
    """
    File viewset
    """
    queryset = File.objects.order_by("-created_at")
    serializer_class = FileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )
    filter_backends = (django_rest_filters.DjangoFilterBackend, )
