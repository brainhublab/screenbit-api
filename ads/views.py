from .models import Ad
from .serializers import AdSerializer, ActiveAdsIdsSerializer
from .permissions import IsAdminUserOrOwner, IsAuthenticatedWorker
from rest_framework import viewsets, filters, serializers
from django.db.models import Q
from django_filters import rest_framework as django_rest_filters
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action
from settings import local_settings
from rest_framework_api_key.permissions import HasAPIKey
from .utils import ad_media_disable, ad_media_loader


class AdViewSet(viewsets.ModelViewSet):
    """
    Advertising viewset
    """
    queryset = Ad.objects.prefetch_related("stadrelation").order_by('-created_at')
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
        if instance.is_active:
            raise serializers.ValidationError({"message":
                                               "Ad is used in activ advertisment. \
                                                Please disable advertisement media before delete"})
        else:
            return super(AdViewSet, self).destroy(request, *args, **kwargs)

    @action(detail=False, permission_classes=[HasAPIKey | IsAdminUserOrOwner], methods=['patch'], url_path='enable/(?P<pk>\d*)')
    def enable(self, request, pk):
        """ Activate ad on screens programs """
        instance = self.get_object()
        ad_media_loader(instance)
        return Response({"message": "Enabaled"}, 200)

    @action(detail=False, permission_classes=[HasAPIKey | IsAdminUserOrOwner], methods=['patch'], url_path='disable/(?P<pk>\d*)')
    def disable(self, request, pk):
        """ Disactivate ad from screens programs """
        instance = self.get_object()
        ad_media_disable(instance)
        return Response({"message": "Disabled"}, 200)

    @action(detail=False, permission_classes=[HasAPIKey | IsAdminUserOrOwner], methods=['get'])
    def areas(self, request):
        """Action that return list of Sofia's areas"""
        if self.request.user:
            return Response({"areas": local_settings.AREAS}, 200)
        else:
            return Response({"message": "Permission denied"}, 403)

    @action(detail=False, permission_classes=[IsAuthenticatedWorker], methods=['get'])
    def active(self, request):
        """Action that return list of active ads for current hour"""
        hour = request.GET.get('hour')
        print(hour)
        active_ads = Ad.objects.filter(is_active=True, hours__icontains=hour)

        print(active_ads)
        serializer = ActiveAdsIdsSerializer(
            active_ads, many=True, context={'request': request})
        return Response(serializer.data)
