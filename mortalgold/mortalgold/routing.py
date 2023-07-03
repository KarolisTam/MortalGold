# routing.py
from django.urls import path
from gameapp.consumers import EchoConsumer

websocket_urlpatterns = [
    path('ws/', EchoConsumer.as_asgi()),
]

