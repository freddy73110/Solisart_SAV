from django.urls import path
from sav.consumers import Cartcreating, production, updateDB

ws_urlpatterns = [
    path(r'ws/cartcreator/', Cartcreating.as_asgi()),
    path(r'ws/production/', production.as_asgi()),
    path(r'ws/updateDB/', updateDB.as_asgi()),
]