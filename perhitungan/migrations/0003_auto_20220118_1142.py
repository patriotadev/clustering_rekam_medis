# Generated by Django 3.2.9 on 2022-01-18 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perhitungan', '0002_auto_20220118_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perhitungan',
            name='usia_anak',
            field=models.BooleanField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='perhitungan',
            name='usia_dewasa',
            field=models.BooleanField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='perhitungan',
            name='usia_manula',
            field=models.BooleanField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='perhitungan',
            name='usia_remaja',
            field=models.BooleanField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='perhitungan',
            name='usia_tua',
            field=models.BooleanField(blank=True, default=0, null=True),
        ),
    ]