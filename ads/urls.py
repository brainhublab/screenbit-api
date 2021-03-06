"""
Advertising urls
"""
from rest_framework import routers
from django.conf.urls import url, include
from . import views

ROUTER = routers.DefaultRouter()
ROUTER.register(r'ads', views.AdViewSet, base_name="ad")

urlpatterns = [
    url(r'', include(ROUTER.urls))
]
