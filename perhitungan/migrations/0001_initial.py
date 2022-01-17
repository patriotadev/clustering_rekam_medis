# Generated by Django 3.2.9 on 2022-01-17 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Perhitungan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_penyakit', models.CharField(blank=True, max_length=255, null=True)),
                ('jumlah_pria', models.IntegerField(blank=True, null=True)),
                ('jumlah_Wanita', models.IntegerField(blank=True, null=True)),
                ('usia_anak', models.BooleanField(blank=True, null=True)),
                ('usia_remaja', models.BooleanField(blank=True, null=True)),
                ('usia_dewasa', models.BooleanField(blank=True, null=True)),
                ('usia_tua', models.BooleanField(blank=True, null=True)),
                ('usia_manula', models.BooleanField(blank=True, null=True)),
                ('c1', models.CharField(blank=True, max_length=255, null=True)),
                ('c2', models.CharField(blank=True, max_length=255, null=True)),
                ('c3', models.CharField(blank=True, max_length=255, null=True)),
                ('kelompok', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
