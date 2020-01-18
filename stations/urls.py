"""
Stations urls
"""
from rest_framework import routers
from django.conf.urls import url, include
from django.urls import path
from . import views

ROUTER = routers.DefaultRouter()
ROUTER.register(r'stations', views.StationViewSet, base_name="station")

urlpatterns = [
    url(r'', include(ROUTER.urls)),
    path('portals/', views.station_portal_view),
]
