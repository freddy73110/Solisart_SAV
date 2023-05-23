from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/livec/$', consumers.Calculator.as_asgi()),
    re_path(r'^ws/mails/(?P<room_name>\w+)/$', consumers.Websock_Mails.as_asgi()),
]