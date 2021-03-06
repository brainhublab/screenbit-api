"""
screenbit core url
"""
from rest_framework import routers
from django.conf.urls import url, include
from . import views

ROUTER = routers.DefaultRouter()
ROUTER.register(r'images', views.ImageViewSet, base_name="image")
ROUTER.register(r'files', views.FileViewSet, base_name="file")

urlpatterns = [
    url(r'', include(ROUTER.urls))
]
