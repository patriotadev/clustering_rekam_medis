from django.db import models

# Create your models here.


class Perhitungan(models.Model):
    nama_penyakit = models.CharField(max_length=255, blank=True, null=True)
    jumlah_laki = models.IntegerField(blank=True, null=True)
    jumlah_perempuan = models.IntegerField(blank=True, null=True)
    usia_anak = models.IntegerField(blank=True, null=True, default=0)
    usia_remaja = models.IntegerField(blank=True, null=True, default=0)
    usia_dewasa = models.IntegerField(blank=True, null=True, default=0)
    usia_tua = models.IntegerField(blank=True, null=True, default=0)
    usia_manula = models.IntegerField(blank=True, null=True, default=0)
    c1 = models.CharField(max_length=255, blank=True, null=True)
    c2 = models.CharField(max_length=255, blank=True, null=True)
    c3 = models.CharField(max_length=255, blank=True, null=True)
    kelompok = models.CharField(max_length=255, blank=True, null=True)


def __str__(self):
    return self.nama_penyakit
