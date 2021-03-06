# Generated by Django 2.1.7 on 2020-06-02 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stations', '0001_initial'),
        ('ads', '0002_ad_creator'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('viewer', 'Viewer'), ('reached', 'Reached'), ('holder', 'Holder'), ('btn_usr', 'Button user')], default='viewer', max_length=100)),
                ('button_clicks', models.IntegerField(null=True)),
                ('duration', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Event', to='ads.Ad')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Event', to='stations.Station')),
            ],
        ),
    ]
