# Generated by Django 3.2.9 on 2022-01-18 02:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perhitungan', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='perhitungan',
            old_name='jumlah_Wanita',
            new_name='jumlah_laki',
        ),
        migrations.RenameField(
            model_name='perhitungan',
            old_name='jumlah_pria',
            new_name='jumlah_perempuan',
        ),
    ]
