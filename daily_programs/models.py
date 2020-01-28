"""Models"""
from django.db import models
from programs.models import Program

from authentication.models import User
from django.utils.translation import ugettext as _


class DailyProgram(models.Model):
    """
    Media program Model
    """
    creator = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='DailyProgram')

    title = models.TextField(max_length=60, null=False, blank=False)
    description = models.TextField(max_length=300, null=False, blank=False)

    program_members = models.ManyToManyField(Program, through='DailyProgramMembership')

    is_in_use = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DailyProgramMembership(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='dailyprmembership')
    daily_program = models.ForeignKey(DailyProgram, on_delete=models.CASCADE, related_name='dailyprmembership')
    start_time = models.TimeField()
    stop_time = models.TimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
