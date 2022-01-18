from http.client import HTTPResponse
from django.http.response import JsonResponse
from urllib import request
from django.core import serializers
from django.shortcuts import render, redirect
from perhitungan.models import Perhitungan
from rm.models import Penyakit, RM

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    perhitungan = Perhitungan.objects.all()
    if request.is_ajax():
        perhitungan_serialized = serializers.serialize('python', perhitungan)
        perhitungan_json = [d['fields'] for d in perhitungan_serialized]
        return JsonResponse(perhitungan_json, safe=False)
    return render(request, 'perhitungan/index.html', {'perhitungan': perhitungan})


def generate(request):
    Perhitungan.objects.all().delete()
    penyakit = Penyakit.objects.values_list('nama_penyakit', flat=True)
    for p in penyakit:
        lk_count = RM.objects.filter(diagnosis__contains=p,
                                     jenis_kelamin='L').count()
        pr_count = RM.objects.filter(diagnosis__contains=p,
                                     jenis_kelamin='P').count()
        kategori_usia = RM.objects.values_list(
            'umur', flat=True).filter(diagnosis__contains=p)

        perhitungan = Perhitungan(
            nama_penyakit=p, jumlah_laki=lk_count, jumlah_perempuan=pr_count)
        perhitungan.save()

        for u in kategori_usia:
            if int(u) <= 11:
                Perhitungan.objects.filter(
                    nama_penyakit=p).update(usia_anak=1)
            elif int(u) >= 12 & int(u) <= 25:
                Perhitungan.objects.filter(
                    nama_penyakit=p).update(usia_remaja=1)
            elif int(u) >= 25 & int(u) <= 45:
                Perhitungan.objects.filter(
                    nama_penyakit=p).update(usia_dewasa=1)
            elif int(u) >= 45 & int(u) <= 65:
                Perhitungan.objects.filter(
                    nama_penyakit=p).update(usia_tua=1)
            elif int(u) > 65:
                Perhitungan.objects.filter(
                    nama_penyakit=p).update(usia_manula=1)

    perhitungan = Perhitungan.objects.all()
    if request.is_ajax():
        perhitungan_serialized = serializers.serialize('python', perhitungan)
        perhitungan_json = [d['fields'] for d in perhitungan_serialized]
        return JsonResponse(perhitungan_json, safe=False)
    return render(request, 'perhitungan/index.html', {'perhitungan': perhitungan})
