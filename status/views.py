from django.shortcuts import render
from django.http import HttpResponse

def status(request):
    return HttpResponse("localhost:8000/status<br>{<br>status:true<br>}")
# Create your views here.
