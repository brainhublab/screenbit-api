from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "bio", "first_name", "last_name", "date_joined", "last_active", )
    search_fields = ("email", "bio", "first_name", "last_name", )
