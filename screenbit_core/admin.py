from django.contrib import admin
from .models import Image, File


# admin.site.register(Image)
# admin.site.register(File)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "content_type", "object_id", "content_object", "image")
    search_fields = ("=content_type", "object_id", "content_object")


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ("id", "content_type", "object_id", "content_object", "file", "created_at", "updated_at")
    search_fields = ("=content_type", "object_id", "content_object")
