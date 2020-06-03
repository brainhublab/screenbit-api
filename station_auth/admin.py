from django.contrib import admin
from .models import StationToken


@admin.register(StationToken)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("token", "station", "created_at", "updated_at")
    search_fields = ("=station__id", )
