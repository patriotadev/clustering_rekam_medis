# Generated by Django 3.2.9 on 2022-01-10 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_pasien', models.CharField(max_length=255)),
                ('jenis_kelamin', models.CharField(max_length=255)),
                ('umur', models.CharField(blank=True, max_length=255, null=True)),
                ('alamat', models.CharField(blank=True, max_length=255, null=True)),
                ('diagnosis', models.CharField(max_length=255)),
            ],
        ),
    ]