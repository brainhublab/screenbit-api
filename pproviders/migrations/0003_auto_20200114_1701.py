# Generated by Django 2.1.7 on 2020-01-14 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pproviders', '0002_auto_20200114_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pprovider',
            name='f_name',
            field=models.TextField(default='tttst', max_length=60),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pprovider',
            name='l_name',
            field=models.TextField(default='llname', max_length=60),
            preserve_default=False,
        ),
    ]
