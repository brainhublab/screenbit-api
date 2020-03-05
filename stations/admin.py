from django.contrib import admin
from .models import Station, StationAdRelation


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ("id", "creator", "pprovider", "title", "description",
                    "city", "area", "viewers", "mac_addr", "net_addr", "p_addr",
                    "lat", "long", "created_at", "updated_at")
    search_fields = ("=creator__id", "pprovider__id", "title", "description", "city",
                     "mac_addr", "net_addr", "p_addr", "lat", "long", )


@admin.register(StationAdRelation)
class StationAdRelationAdmin(admin.ModelAdmin):
    list_display = ("ad", "station", "hour", "created_at", "updated_at")
    search_fields = ("=station__id", "=ad__id", "=hour")
