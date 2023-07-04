from django.urls import re_path

from gameapp.consumers import EchoConsumer

websocket_urlpatterns = [
    re_path(r'ws/$', EchoConsumer.as_asgi()),
]