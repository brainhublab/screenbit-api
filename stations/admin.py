from django.contrib import admin
from .models import Station, StationProgramRelation


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ("creator", "pprovider", "title", "description", "city",
                    "mac_addr", "net_addr", "p_addr", "lat", "long", "created_at", "updated_at")
    search_fields = ("=creator__id", "pprovider__id", "title", "description", "city",
                     "mac_addr", "net_addr", "p_addr", "lat", "long", )


@admin.register(StationProgramRelation)
class StationProgramRelationAdmin(admin.ModelAdmin):
    list_display = ("program", "station", "hour", "created_at", "updated_at")
    search_fields = ("=station__id", "=program__id", "=hour")
