from django.shortcuts import render
from django.views import View



def index(request):
    return render(request, 'gameapp/index.html')

