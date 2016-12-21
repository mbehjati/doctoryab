# Create your views here.
from django.shortcuts import render


def index(request):
    return render(request, 'appointment/set_doctor_free_times.html')
