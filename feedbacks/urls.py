"""
Advertising urls
"""
from rest_framework import routers
from django.conf.urls import url, include
from . import views

ROUTER = routers.DefaultRouter()
ROUTER.register(r'feedbacks', views.FeedbackViewSet, base_name="feedback")

urlpatterns = [
    url(r'', include(ROUTER.urls))
]
