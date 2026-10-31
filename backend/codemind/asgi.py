"""
ASGI config for codemind project.
Enables async WebSocket protocol routing and HTTP handling via Channels & Daphne.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codemind.settings')

# Initialize Django ASGI application early to ensure AppRegistry is populated
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import snippets.routing

application = ProtocolTypeRouter({
    # Standard HTTP requests handled by Django ASGI
    "http": django_asgi_app,
    
    # Real-Time WebSocket connections handled by Channels & SnippetRoomConsumer
    "websocket": AuthMiddlewareStack(
        URLRouter(
            snippets.routing.websocket_urlpatterns
        )
    ),
})
