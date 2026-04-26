from django.urls import re_path
from . import consumers

# maps websocket url to consumer (similar to urls.py)
websocket_patterns = [
    re_path(r'ws/chat/channel/(?P<channel_uid>[0-9a-f-]+)/$', consumers.ChatConsumer.as_asgi()),
]