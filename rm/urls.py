from django.urls.conf import path
from rm import views

app_name = 'rm'
urlpatterns = [
    path('pasien', views.pasien_index, name='pasien'),
    path('penyakit', views.penyakit_index, name='penyakit'),
    path('penyakit/klasifikasi', views.klasifikasi_index, name='klasifikasi'),
    path('upload', views.rm_upload, name='rm_upload'),
    path('penyakit/klasifikasi/upload',
         views.klasifikasi_upload, name='klasifikasi_upload')
]
