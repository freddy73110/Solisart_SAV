import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
# from one.routing import ws_urlpatterns
import sav.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Solisart_SAV.settings')

application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  'websocket': AuthMiddlewareStack(
        URLRouter(
            sav.routing.ws_urlpatterns
        )
    ),
})

