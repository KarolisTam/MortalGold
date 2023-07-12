from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('match/', views.MatchCreateList.as_view()),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    
    path('', views.index, name='index'),
    path('<str:match_id>/', views.room, name='room'),
]