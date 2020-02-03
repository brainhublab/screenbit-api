# Generated by Django 2.1.7 on 2020-01-30 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=60)),
                ('description', models.TextField(max_length=300)),
                ('media_type', models.CharField(choices=[('VD', 'Video media type'), ('IM', 'Image media type'), ('GF', 'GIF media type')], max_length=2, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Ad', to='clients.Client')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Ad', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
