from django.contrib import admin
from .models import Event


@admin.register(Event)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "station", "ad", "type", "duration", "button_clicks", "created_at")
    search_fields = ("=station__id", "=ad__id")
