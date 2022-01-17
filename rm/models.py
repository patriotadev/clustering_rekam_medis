from asyncio.windows_events import NULL
from django.db import models

# Create your models here.


class RM(models.Model):
    nama_pasien = models.CharField(max_length=255, blank=False, null=False)
    jenis_kelamin = models.CharField(max_length=255, blank=False, null=False)
    umur = models.CharField(max_length=255, blank=True, null=True)
    alamat = models.CharField(max_length=255, blank=True, null=True)
    diagnosis = models.CharField(max_length=255, blank=False, null=False)
    kode_diagnosis = models.CharField(
        max_length=255, blank=False, null=False, default=NULL)

    def __str__(self):
        return self.nama_pasien


class Penyakit(models.Model):
    kode_penyakit = models.CharField(max_length=255, blank=True, null=True)
    bab_penyakit = models.CharField(max_length=255, blank=True, null=True)
    nama_penyakit = models.CharField(max_length=255, blank=True, null=True)
    jenis_penyakit = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.kode_penyakit


class Klasifikasi(models.Model):
    bab = models.CharField(max_length=255, blank=True, null=True)
    blok = models.CharField(max_length=255, blank=True, null=True)
    jenis = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.jenis
