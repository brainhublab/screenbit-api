# Generated by Django 2.1.7 on 2020-02-27 14:24

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='areas',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('1618', 'Bakston'), ('1233', 'Banishora'), ('1680', 'Beli brezi'), ('1278', 'Benkovski'), ('1680', 'Borovo'), ('1870', 'Botunets'), ('1616', 'Boyana'), ('1853', 'Chelopechene'), ('1756', 'Darvenitsa'), ('1172', 'Dianabad'), ('1415', 'Dragalevtsi'), ('1592', 'Drujba 1'), ('1582', 'Drujba 2'), ('1373', 'Fakulteta'), ('1390', 'Filipovtsi'), ('1574', 'Geo Milev'), ('1614', 'Gorna Banya'), ('1138', 'Gorublyane'), ('1404', 'Gotse Delchev'), ('1510', 'Hadji Dimitar'), ('1612', 'Hipodruma'), ('1407', 'Hladilnika'), ('1517', 'Hristo Botev'), ('1271', 'Iliantsi'), ('1408', 'Ivan Vazov'), ('1113', 'Izgrev'), ('1113', 'Iztok'), ('1619', 'Knyajevo'), ('1330', 'Krasna Polyana'), ('1618', 'Krasno Selo'), ('1849', 'Kremikovtsi'), ('1612', 'Lagera'), ('1836', 'Levski'), ('1421', 'Lozenets'), ('1360', 'Lyulin 1'), ('1335', 'Lyulin 10'), ('1343', 'Lyulin 2'), ('1336', 'Lyulin 3'), ('1359', 'Lyulin 4'), ('1359', 'Lyulin 5'), ('1336', 'Lyulin 6'), ('1324', 'Lyulin 7'), ('1336', 'Lyulin 8'), ('1324', 'Lyulin 9'), ('1225', 'Malashevtsi'), ('1797', 'Malinova Dolina'), ('1404', 'Manastirski Livadi'), ('1784', 'Mladost 1'), ('1799', 'Mladost 2'), ('1712', 'Mladost 3'), ('1715', 'Mladost 4'), ('1360', 'Moderno predgradie'), ('1404', 'Motopista'), ('1797', 'Musagenitsa'), ('1220', 'Nadejda'), ('1229', 'Nadejda 3'), ('1231', 'Nadejda 6'), ('1387', 'Obelya'), ('1326', 'Obelya 2'), ('1618', 'Ovcha kupel'), ('1632', 'Ovcha kupel 2'), ('1618', 'Pavlovo'), ('1517', 'Poduyane'), ('1784', 'Poligona'), ('1506', 'Reduta'), ('1301', 'Republika'), ('1808', 'Seslavtsi'), ('1434', 'Simeonovo'), ('1574', 'Slatina'), ('1510', 'Stefan Karadja'), ('1404', 'Strelbishte'), ('1700', 'Studentski grad'), ('1505', 'Suhata Reka'), ('1362', 'Suhodol'), ('1309', 'Sveta Troitsa'), ('1298', 'Trebich'), ('1839', 'Vrajdebna'), ('1111', 'Yavorov'), ('1345', 'Zaharna fabrika'), ('1373', 'Zapaden Park'), ('1309', 'Zona B-18'), ('1330', 'Zona B-19'), ('1303', 'Zona B-5')], max_length=4, null=True), null=True, size=24),
        ),
        migrations.AddField(
            model_name='ad',
            name='hours',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('00', 'TWELVE AM'), ('01', 'ОNЕ AM'), ('02', 'TWO AM'), ('03', 'THREE AM'), ('04', 'FOUR AM'), ('05', 'FIVE AM'), ('06', 'SIX AM'), ('07', 'SEVEN AM'), ('08', 'EIGHT AM'), ('09', 'NINE AM'), ('10', 'TEN AM'), ('11', 'ELEVEN AM'), ('12', 'TWELVE PM'), ('13', 'ОНЕ PM'), ('14', 'TWO PM'), ('15', 'THREE PM'), ('16', 'FOUR PM'), ('17', 'FIVE PM'), ('18', 'SIX PM'), ('19', 'SEVEN PM'), ('20', 'EIGHT PM'), ('21', 'NINE PM'), ('22', 'TEN PM'), ('23', 'ELEVEN PM')], max_length=2, null=True), null=True, size=24),
        ),
    ]
