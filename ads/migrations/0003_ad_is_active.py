# Generated by Django 2.1.7 on 2020-02-27 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_auto_20200227_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]