from django.contrib import admin
from .models import Ad


@admin.register(Ad)
class AdsAdmin(admin.ModelAdmin):
    list_display = ("creator", "title", "description", "media_type", "created_at", "updated_at")
    search_fields = ("=creator__id", "title", "description", "media_type", )
