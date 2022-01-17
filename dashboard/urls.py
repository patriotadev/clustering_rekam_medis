from django.urls.conf import path
from dashboard import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout_view, name='logout')
]
