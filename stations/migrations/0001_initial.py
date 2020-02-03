# Generated by Django 2.1.7 on 2020-01-30 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('programs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pproviders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=60)),
                ('description', models.TextField(max_length=300)),
                ('city', models.CharField(choices=[('SO', 'Sofia city'), ('BS', 'Burgas city'), ('PL', 'Plovdiv city'), ('VA', 'Varna city')], max_length=2, null=True)),
                ('mac_addr', models.TextField(max_length=300, unique=True)),
                ('net_addr', models.TextField(blank=True, max_length=300, unique=True)),
                ('p_addr', models.TextField(blank=True, max_length=300)),
                ('lat', models.DecimalField(decimal_places=7, max_digits=9, null=True)),
                ('long', models.DecimalField(decimal_places=7, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Station', to=settings.AUTH_USER_MODEL)),
                ('pprovider', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Station', to='pproviders.Pprovider')),
            ],
        ),
        migrations.CreateModel(
            name='StationProgramRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hour', models.CharField(choices=[('00', 'TWELVE AM'), ('01', 'ОNЕ AM'), ('02', 'TWO AM'), ('03', 'THREE AM'), ('04', 'FOUR AM'), ('05', 'FIVE AM'), ('06', 'SIX AM'), ('07', 'SEVEN AM'), ('08', 'EIGHT AM'), ('09', 'NINE AM'), ('10', 'TEN AM'), ('11', 'ELEVEN AM'), ('12', 'TWELVE PM'), ('13', 'ОНЕ PM'), ('14', 'TWO PM'), ('15', 'THREE PM'), ('16', 'FOUR PM'), ('17', 'FIVE PM'), ('18', 'SIX PM'), ('19', 'SEVEN PM'), ('20', 'EIGHT PM'), ('21', 'NINE PM'), ('22', 'TEN PM'), ('23', 'ELEVEN PM')], max_length=2, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stprrelation', to='programs.Program')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stprrelation', to='stations.Station')),
            ],
        ),
        migrations.AddField(
            model_name='station',
            name='programs',
            field=models.ManyToManyField(through='stations.StationProgramRelation', to='programs.Program'),
        ),
        migrations.AlterUniqueTogether(
            name='stationprogramrelation',
            unique_together={('station', 'hour')},
        ),
    ]
