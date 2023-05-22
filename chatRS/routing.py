from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path("ws/chat/(?P<rcode>\w+)/(?P<uid>\w+)/$", consumers.ChatConsumer.as_asgi()),
]