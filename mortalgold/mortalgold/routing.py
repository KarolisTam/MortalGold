#routing.py
from django.urls import re_path
from gameapp.consumers import GameConsumer


websocket_urlpatterns = [
    re_path(r'ws/game/(?P<match_id>\d+)/$', GameConsumer.as_asgi()),
]

