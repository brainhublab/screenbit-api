# Generated by Django 2.1.7 on 2020-06-02 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='hour',
            field=models.CharField(choices=[('00', 'TWELVE AM'), ('01', 'ОNЕ AM'), ('02', 'TWO AM'), ('03', 'THREE AM'), ('04', 'FOUR AM'), ('05', 'FIVE AM'), ('06', 'SIX AM'), ('07', 'SEVEN AM'), ('08', 'EIGHT AM'), ('09', 'NINE AM'), ('10', 'TEN AM'), ('11', 'ELEVEN AM'), ('12', 'TWELVE PM'), ('13', 'ОНЕ PM'), ('14', 'TWO PM'), ('15', 'THREE PM'), ('16', 'FOUR PM'), ('17', 'FIVE PM'), ('18', 'SIX PM'), ('19', 'SEVEN PM'), ('20', 'EIGHT PM'), ('21', 'NINE PM'), ('22', 'TEN PM'), ('23', 'ELEVEN PM')], default='00', max_length=2, null=True),
        ),
    ]
