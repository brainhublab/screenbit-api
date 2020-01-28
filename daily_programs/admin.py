from django.contrib import admin
from .models import DailyProgram, DailyProgramMembership


# Register your models here.
admin.site.register(DailyProgram)
admin.site.register(DailyProgramMembership)
