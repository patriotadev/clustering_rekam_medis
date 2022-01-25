import math
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.core import serializers
from django.shortcuts import redirect, render
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
            nama_penyakit=p, jumlah_laki=lk_count, jumlah_perempuan=pr_count, iteration=1)
        perhitungan.save()
        for u in kategori_usia:
            if float(u) <= 11:
                Perhitungan.objects.filter(
                    nama_penyakit=p).update(usia_anak=1)
            elif 11 < float(u) < 26:
                Perhitungan.objects.filter(
                    nama_penyakit=p).update(usia_remaja=1)
            elif 25 < float(u) < 46:
                Perhitungan.objects.filter(
                    nama_penyakit=p).update(usia_dewasa=1)
            elif 45 < float(u) < 66:
                Perhitungan.objects.filter(
                    nama_penyakit=p).update(usia_tua=1)
            else:
                Perhitungan.objects.filter(
                    nama_penyakit=p).update(usia_manula=1)

    perhitungan = Perhitungan.objects.all()
    if request.is_ajax():
        perhitungan_serialized = serializers.serialize('python', perhitungan)
        perhitungan_json = [d['fields'] for d in perhitungan_serialized]
        return JsonResponse(perhitungan_json, safe=False)
    return render(request, 'perhitungan/index.html', {'perhitungan': perhitungan})


def proses(request):
    dataSet = Perhitungan.objects.filter(iteration=1).values_list()
    dataCount = Perhitungan.objects.filter(iteration=1).count()
    initCentroid = Perhitungan.objects.order_by('?')[:3].values_list()

    # --> Cluster 1
    centroid1 = initCentroid[0]
    cluster1 = list()
    for n in range(dataCount):
        cluster1_list = 0
        cluster1_temp = 0
        for l in range(2, 9):
            cluster1_list = math.pow(dataSet[n][l] - centroid1[l], 2)
            cluster1_temp += cluster1_list
        cluster1.append(math.sqrt(cluster1_temp))
    for d, data in zip(range(dataCount), dataSet):
        Perhitungan.objects.filter(
            iteration=1, id=data[0]).update(c1=cluster1[d])

    # --> Cluster 2
    centroid2 = initCentroid[1]
    cluster2 = list()
    for n in range(dataCount):
        cluster2_list = 0
        cluster2_temp = 0
        for l in range(2, 9):
            cluster2_list = math.pow(dataSet[n][l] - centroid2[l], 2)
            cluster2_temp += cluster2_list
        cluster2.append(math.sqrt(cluster2_temp))
    for d, data in zip(range(dataCount), dataSet):
        Perhitungan.objects.filter(
            iteration=1, id=data[0]).update(c2=cluster2[d])

    # --> Cluster 3
    centroid3 = initCentroid[2]
    cluster3 = list()
    for n in range(dataCount):
        cluster3_list = 0
        cluster3_temp = 0
        for l in range(2, 9):
            cluster3_list = math.pow(dataSet[n][l] - centroid3[l], 2)
            cluster3_temp += cluster3_list
        cluster3.append(math.sqrt(cluster3_temp))
    for d, data in zip(range(dataCount), dataSet):
        Perhitungan.objects.filter(
            iteration=1, id=data[0]).update(c3=cluster3[d])

    # --> Get Cluster Group
    dataSet = Perhitungan.objects.filter(iteration=1).values_list()
    kelompok = list()
    for d in range(dataCount):
        if (float(dataSet[d][9]) <= float(dataSet[d][10])) and (float(dataSet[d][9]) <= float(dataSet[d][11])):
            kelompok.append('C1')
        elif (float(dataSet[d][10]) <= float(dataSet[d][9])) and (float(dataSet[d][10]) <= float(dataSet[d][11])):
            kelompok.append('C2')
        elif (float(dataSet[d][11]) <= float(dataSet[d][9])) and (float(dataSet[d][11]) <= float(dataSet[d][10])):
            kelompok.append('C3')
    for d, data in zip(range(dataCount), dataSet):
        Perhitungan.objects.filter(
            iteration=1, id=data[0]).update(kelompok=kelompok[d])

    return HttpResponse(dataSet)
