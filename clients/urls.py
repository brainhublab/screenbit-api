"""
Client urls
"""
from rest_framework import routers
from django.conf.urls import url, include
from . import views

ROUTER = routers.DefaultRouter()
ROUTER.register(r'clients', views.ClientViewSet, base_name="client")

urlpatterns = [
    url(r'', include(ROUTER.urls))
]
