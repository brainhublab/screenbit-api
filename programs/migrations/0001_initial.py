# Generated by Django 2.1.7 on 2020-01-16 13:34

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=60)),
                ('description', models.TextField(max_length=300)),
                ('ad_ids', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, null=True, size=None)),
                ('media_urls', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=list, null=True, size=None)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Program', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]