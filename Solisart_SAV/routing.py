from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import sav.routing
from django.core.asgi import get_asgi_application
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Solisart_SAV.settings")

print('print', sav.routing.websocket_urlpatterns)

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            sav.routing.websocket_urlpatterns
        )
    ),
})