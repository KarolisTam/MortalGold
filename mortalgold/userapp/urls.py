from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.singup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
]
