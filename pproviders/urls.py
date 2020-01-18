"""
PlaceProvider urls
"""
from rest_framework import routers
from django.conf.urls import url, include
from . import views

ROUTER = routers.DefaultRouter()
ROUTER.register(r'pproviders', views.PlaceProviderViewSet, base_name="pprovider")

urlpatterns = [
    url(r'', include(ROUTER.urls))
]
