"""
Program urls
"""
from rest_framework import routers
from django.conf.urls import url, include
from . import views

ROUTER = routers.DefaultRouter()
ROUTER.register(r'daily_programs', views.DailyProgramViewSet, base_name="dailyprogram")

urlpatterns = [
    url(r'', include(ROUTER.urls)),
]
