# Generated by Django 2.1.7 on 2020-02-13 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('station_auth', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stationtoken',
            old_name='statoin',
            new_name='statiоn',
        ),
    ]
