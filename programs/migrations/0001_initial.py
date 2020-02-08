# Generated by Django 2.1.7 on 2020-02-05 12:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ads', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=60)),
                ('description', models.TextField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProgramAdMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad_index', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pradmembership', to='ads.Ad')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pradmembership', to='programs.Program')),
            ],
        ),
        migrations.AddField(
            model_name='program',
            name='ad_members',
            field=models.ManyToManyField(through='programs.ProgramAdMembership', to='ads.Ad'),
        ),
        migrations.AddField(
            model_name='program',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Program', to=settings.AUTH_USER_MODEL),
        ),
    ]
