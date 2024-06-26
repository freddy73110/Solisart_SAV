from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import sav.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            sav.routing.ws_urlpatterns
        )
    ),
})