import math
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.core import serializers
from django.shortcuts import redirect, render
from perhitungan.models import Perhitungan
from rm.models import Penyakit, RM
import numpy as np

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    perhitungan = Perhitungan.objects.filter(iteration=1)
    if request.is_ajax():
        perhitungan_serialized = serializers.serialize('python', perhitungan)
        perhitungan_json = [d['fields'] for d in perhitungan_serialized]
        return JsonResponse(perhitungan_json, safe=False)
    return render(request, 'perhitungan/index.html', {'perhitungan': perhitungan})


def generate(request):
    if not request.user.is_authenticated:
        return redirect('login')
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
    if not request.user.is_authenticated:
        return redirect('login')
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

    # Iteration Count
    dataSet = Perhitungan.objects.filter(
        iteration=1).order_by('id').values_list()
    i = 2
    while not Perhitungan.objects.filter(iteration__gt=1) or equal_value == False:
        for data in dataSet:
            Perhitungan(
                nama_penyakit=data[1], jumlah_laki=data[2], jumlah_perempuan=data[3], usia_anak=data[4], usia_remaja=data[5], usia_dewasa=data[6], usia_tua=data[7], usia_manula=data[8], iteration=i).save()

        # --> Get cluster 1 centroid
        centroid1 = Perhitungan.objects.filter(
            kelompok='C1', iteration=i-1).values_list()
        centroid1_count = Perhitungan.objects.filter(
            kelompok='C1', iteration=i-1).count()
        centroid1_list = list()
        for c in range(2, 9):
            column_temp = 0
            for data in centroid1:
                print(data[c], data[1])
                column_temp += data[c]
            centroid1_list.append(column_temp / centroid1_count)
        print(centroid1_list)

        # --> Get cluster 2 centroid
        centroid2 = Perhitungan.objects.filter(
            kelompok='C2', iteration=i-1).values_list()
        centroid2_count = Perhitungan.objects.filter(
            kelompok='C2', iteration=i-1).count()
        centroid2_list = list()
        for c in range(2, 9):
            column_temp = 0
            for data in centroid2:
                print(data[c], data[1])
                column_temp += data[c]
            centroid2_list.append(column_temp / centroid2_count)
        print(centroid2_list)

        # --> Get cluster 3 centroid
        centroid3 = Perhitungan.objects.filter(
            kelompok='C3', iteration=i-1).values_list()
        centroid3_count = Perhitungan.objects.filter(
            kelompok='C3', iteration=i-1).count()
        centroid3_list = list()
        for c in range(2, 9):
            column_temp = 0
            for data in centroid3:
                print(data[c], data[1])
                column_temp += data[c]
            centroid3_list.append(column_temp / centroid3_count)
        print(centroid3_list)

        # --> Euclidean Distance for iteration > 1
        dataSet = Perhitungan.objects.filter(iteration=i).values_list()
        dataCount = Perhitungan.objects.filter(iteration=i).count()

        # --> Cluster 1
        centroid1 = centroid1_list
        cluster1 = list()
        for n in range(dataCount):
            cluster1_list = 0
            cluster1_temp = 0
            for l, r in zip(range(2, 9), range(7)):
                cluster1_list = math.pow(dataSet[n][l] - centroid1[r], 2)
                cluster1_temp += cluster1_list
            cluster1.append(math.sqrt(cluster1_temp))
        for d, data in zip(range(dataCount), dataSet):
            Perhitungan.objects.filter(
                iteration=i, id=data[0]).update(c1=cluster1[d])

        # --> Cluster 2
        centroid2 = centroid2_list
        cluster2 = list()
        for n in range(dataCount):
            cluster2_list = 0
            cluster2_temp = 0
            for l, r in zip(range(2, 9), range(7)):
                cluster2_list = math.pow(dataSet[n][l] - centroid2[r], 2)
                cluster2_temp += cluster2_list
            cluster2.append(math.sqrt(cluster2_temp))
        for d, data in zip(range(dataCount), dataSet):
            Perhitungan.objects.filter(
                iteration=i, id=data[0]).update(c2=cluster2[d])

        # --> Cluster 3
        centroid3 = centroid3_list
        cluster3 = list()
        for n in range(dataCount):
            cluster3_list = 0
            cluster3_temp = 0
            for l, r in zip(range(2, 9), range(7)):
                cluster3_list = math.pow(dataSet[n][l] - centroid3[r], 2)
                cluster3_temp += cluster3_list
            cluster3.append(math.sqrt(cluster3_temp))
        for d, data in zip(range(dataCount), dataSet):
            Perhitungan.objects.filter(
                iteration=i, id=data[0]).update(c3=cluster3[d])

        # --> Get Cluster Group
        dataSet = Perhitungan.objects.filter(iteration=i).values_list()
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
                iteration=i, id=data[0]).update(kelompok=kelompok[d])

        # --> Stop iteration IF
        current_iteration = Perhitungan.objects.filter(
            iteration=i).order_by('id').values_list('kelompok')
        last_iteration = Perhitungan.objects.filter(
            iteration=i-1).order_by('id').values_list('kelompok')

        current_iteration_array = np.array([current_iteration])
        last_iteration_array = np.array([last_iteration])

        compare_iteration = current_iteration_array == last_iteration_array
        equal_value = compare_iteration.all()

        print(current_iteration_array)
        print(last_iteration_array)
        print(equal_value)

        i += 1

    return HttpResponse(dataSet)
