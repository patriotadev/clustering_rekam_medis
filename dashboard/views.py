from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'dashboard/index.html')


def logout_view(request):
    logout(request)
    return redirect('login')
