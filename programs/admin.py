from django.contrib import admin
from .models import Program, ProgramAdMembership


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("creator", "title", "description", "created_at", "updated_at")
    search_fields = ("=creator__id", "title", "description", )


@admin.register(ProgramAdMembership)
class ProgramAdMembershipAdmin(admin.ModelAdmin):
    list_display = ("ad", "program", "ad_index", "created_at", "updated_at")
    search_fields = ("=ad__id", "=program__id")
