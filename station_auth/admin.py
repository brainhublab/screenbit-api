from django.contrib import admin
from .models import StationToken


class FeedbackAdmin(admin.ModelAdmin):
    search_fields = ("=station__id", )


# Register your models here.
admin.site.register(StationToken, FeedbackAdmin)
