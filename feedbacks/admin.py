from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "station", "ad", "created_at", "updated_at")
    search_fields = ("=station__id", "=ad__id", )
