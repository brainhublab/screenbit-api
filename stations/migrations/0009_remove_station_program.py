# Generated by Django 2.1.7 on 2020-01-17 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0008_remove_station_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='station',
            name='program',
        ),
    ]