# Generated by Django 2.1.7 on 2020-01-17 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0010_station_program'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]