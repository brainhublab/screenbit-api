# Generated by Django 2.1.7 on 2020-01-19 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0005_remove_program_ad_ids'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='program',
            name='media_data',
        ),
    ]
