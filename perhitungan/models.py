from django.db import models

# Create your models here.


class Perhitungan(models.Model):
    nama_penyakit = models.CharField(max_length=255, blank=True, null=True)
    jumlah_pria = models.IntegerField(blank=True, null=True)
    jumlah_Wanita = models.IntegerField(blank=True, null=True)
    usia_anak = models.BooleanField(blank=True, null=True)
    usia_remaja = models.BooleanField(blank=True, null=True)
    usia_dewasa = models.BooleanField(blank=True, null=True)
    usia_tua = models.BooleanField(blank=True, null=True)
    usia_manula = models.BooleanField(blank=True, null=True)
    c1 = models.CharField(max_length=255, blank=True, null=True)
    c2 = models.CharField(max_length=255, blank=True, null=True)
    c3 = models.CharField(max_length=255, blank=True, null=True)
    kelompok = models.CharField(max_length=255, blank=True, null=True)


def __str__(self):
    return self.nama_penyakit
