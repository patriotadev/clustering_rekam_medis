from ntpath import join
from posixpath import split
from django.core import serializers
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from tablib import Dataset
from import_export import resources
from rm.models import RM, Klasifikasi, Penyakit
# Create your views here.


def pasien_index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    rm = RM.objects.all()
    if request.is_ajax():
        rm_serialized = serializers.serialize('python', rm)
        rm_json = [d['fields'] for d in rm_serialized]
        return JsonResponse(rm_json, safe=False)
    return render(request, 'rm/pasien.html', {'rm': rm})


def penyakit_index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    penyakit = Penyakit.objects.all()
    if request.is_ajax():
        penyakit_serialized = serializers.serialize('python', penyakit)
        penyakit_json = [d['fields'] for d in penyakit_serialized]
        return JsonResponse(penyakit_json, safe=False)
    return render(request, 'rm/penyakit.html', {'penyakit': penyakit})


def klasifikasi_index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    klasifikasi = Klasifikasi.objects.all()
    if request.is_ajax():
        kl_serialized = serializers.serialize('python', klasifikasi)
        kl_json = [d['fields'] for d in kl_serialized]
        return JsonResponse(kl_json, safe=False)
    return render(request, 'rm/klasifikasi.html', {'klasifikasi': klasifikasi})


def rm_upload(request):
    # --> Upload file .xlsx
    if request.method == 'POST' and request.FILES.get('uploaded_file'):
        rm_file = request.FILES['uploaded_file']
        fss = FileSystemStorage(location='static/files/rm/')
        if fss.exists('rm.xlsx'):
            fss.delete('rm.xlsx')
    fss.save('rm.xlsx', rm_file)

    # --> Delete old data
    if request.method == 'POST':
        rm = RM.objects.all()
        rm.delete()
        penyakit = Penyakit.objects.all()
        penyakit.delete()

    # --> Store new data to database (rm_rm)
    if request.method == 'POST':
        rm_resource = resources.modelresource_factory(model=RM)()
        header = ['nama_pasien', 'jenis_kelamin',
                  'umur', 'alamat', 'diagnosis', 'kode_diagnosis']
        with open('static/files/rm/rm.xlsx', 'rb') as fh:
            imported_data = Dataset().load(fh, 'xlsx', headers=header)
            result = rm_resource.import_data(imported_data, dry_run=True)
            if not result.has_errors():
                rm_resource.import_data(imported_data, dry_run=False)

    # --> Store new data to database (rm_penyakit)
    if request.method == 'POST':
        kode_penyakit = RM.objects.values_list('kode_diagnosis', flat=True)
        nama_penyakit = RM.objects.values_list('diagnosis', flat=True)
        kode_penyakit_join = ' '.join(kode_penyakit).split()
        nama_penyakit_join = ' '.join(nama_penyakit).split()
        print(nama_penyakit_join)
        for kp, np in zip(kode_penyakit_join, nama_penyakit_join):
            if Penyakit.objects.filter(kode_penyakit__contains=kp) | Penyakit.objects.filter(nama_penyakit__contains=np):
                None
            else:
                if 'A' in kp:
                    penyakit = Penyakit(
                        kode_penyakit=kp, nama_penyakit=np, bab_penyakit='I', jenis_penyakit='Gangguan A')
                elif 'B' in kp:
                    penyakit = Penyakit(
                        kode_penyakit=kp, nama_penyakit=np, bab_penyakit='II', jenis_penyakit='Gangguan B')
                elif 'C' in kp:
                    penyakit = Penyakit(
                        kode_penyakit=kp, nama_penyakit=np, bab_penyakit='III', jenis_penyakit='Gangguan C')
                elif 'D' in kp:
                    penyakit = Penyakit(
                        kode_penyakit=kp, nama_penyakit=np, bab_penyakit='IV', jenis_penyakit='Gangguan D')
                penyakit.save()

    return HttpResponse(result)


def klasifikasi_upload(request):
    # --> Upload file .xlsx
    if request.method == 'POST' and request.FILES.get('uploaded_file'):
        klasifikasi_file = request.FILES['uploaded_file']
        fss = FileSystemStorage(location='static/files/rm/')
        if fss.exists('klasifikasi.xlsx'):
            fss.delete('klasifikasi.xlsx')
    fss.save('klasifikasi.xlsx', klasifikasi_file)

    # --> Delete old data
    if request.method == 'POST':
        klasifikasi = Klasifikasi.objects.all()
        klasifikasi.delete()

    # --> Store new data to database
    if request.method == 'POST':
        klasifikasi_resource = resources.modelresource_factory(
            model=Klasifikasi)()
        header = ['bab', 'blok',
                  'jenis']
        with open('static/files/rm/klasifikasi.xlsx', 'rb') as fh:
            imported_data = Dataset().load(fh, 'xlsx', headers=header)
            result = klasifikasi_resource.import_data(
                imported_data, dry_run=True)
            if not result.has_errors():
                klasifikasi_resource.import_data(imported_data, dry_run=False)
    return HttpResponse(result)
