from unicodedata import name
from django.urls.conf import path
from perhitungan import views

app_name = 'perhitungan'

urlpatterns = [
    path('', views.index, name='index'),
    path('generate', views.generate, name='generate'),
    path('proses', views.proses, name='proses')
]
