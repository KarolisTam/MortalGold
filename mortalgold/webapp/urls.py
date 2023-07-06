from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('htp/', views.htp, name='htp'),
    path('downloads/', views.downloads, name='downloads'),
    path('tops/', views.tops, name='tops'),
]