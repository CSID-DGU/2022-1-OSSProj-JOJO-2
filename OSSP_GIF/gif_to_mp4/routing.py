# chat/routing.py
from django.urls import re_path

from . import sockets

websocket_urlpatterns = [
    re_path(r'', sockets.GifConsumer.as_asgi()),
]