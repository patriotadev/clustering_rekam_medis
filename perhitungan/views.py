from urllib import request
from django.shortcuts import render
from rm.models import Penyakit

# Create your views here.


def index(request):
    return render(request, 'perhitungan/index.html')


def generate(request):
    penyakit = Penyakit.objects.values_list('nama_penyakit', flat=True)
    print(penyakit)

    return
