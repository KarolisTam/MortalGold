from django.shortcuts import render

def index(request):
    return render(request, 'webapp/index.html')

def htp(request):
    return render(request, 'webapp/htp.html')

def downloads(request):
    return render(request, 'webapp/downloads.html')

def tops(request):
    return render(request, 'webapp/tops.html')
