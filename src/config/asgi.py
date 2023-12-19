"""
ASGI config for finio project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
# DON'T ADD ANYTHING ABOVE THIS LINE
# DON'T ADD ANYTHING ABOVE THIS LINE
# DON'T ADD ANYTHING ABOVE THIS LINE

# from channels.auth import AuthMiddlewareStack
from config.asgiauth import TokenAuthMiddleware
from django.core.asgi import get_asgi_application
from config.routing import websocket_urlpatterns
from channels.routing import get_default_application

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
            TokenAuthMiddleware(URLRouter(websocket_urlpatterns))
        ),
})
print('ASGI application loaded')
print("websocket_urlpatterns: ", websocket_urlpatterns)


# application = get_asgi_application()
