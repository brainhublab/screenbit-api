# Generated by Django 2.1.7 on 2020-06-02 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('station_auth', '0003_auto_20200602_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stationtoken',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='stationtoken',
            name='token',
            field=models.CharField(max_length=250, primary_key=True, serialize=False, verbose_name='Token'),
        ),
    ]
