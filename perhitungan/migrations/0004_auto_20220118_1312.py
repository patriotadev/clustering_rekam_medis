# Generated by Django 3.2.9 on 2022-01-18 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perhitungan', '0003_auto_20220118_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perhitungan',
            name='usia_anak',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='perhitungan',
            name='usia_dewasa',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='perhitungan',
            name='usia_manula',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='perhitungan',
            name='usia_remaja',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='perhitungan',
            name='usia_tua',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
