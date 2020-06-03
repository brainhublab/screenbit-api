"""
Event urls
"""
from rest_framework import routers
from django.conf.urls import url, include
from . import views

ROUTER = routers.DefaultRouter()
ROUTER.register(r'events', views.EventViewSet, base_name="event")

urlpatterns = [
    url(r'', include(ROUTER.urls))
]
