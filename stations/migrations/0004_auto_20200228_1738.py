# Generated by Django 2.1.7 on 2020-02-28 15:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0003_station_viewers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='p_addr',
            field=models.TextField(blank=True, max_length=300, verbose_name='Physical address'),
        ),
        migrations.AlterField(
            model_name='station',
            name='pprovider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='StationPlaceProvider', to=settings.AUTH_USER_MODEL, verbose_name='Place provider'),
        ),
    ]