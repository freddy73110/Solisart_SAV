from django.urls import path
from sav.consumers import Cartcreating

ws_urlpatterns = [
    path(r'ws/cartcreator/', Cartcreating.as_asgi()),
]