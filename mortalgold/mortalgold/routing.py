from django.urls import re_path

from gameapp.consumers import GameConsumer

websocket_urlpatterns = [
    re_path(r'ws/$', GameConsumer.as_asgi()),
]