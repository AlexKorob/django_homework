from channels.routing import ProtocolTypeRouter, URLRouter
from .consumers import NotificationConsumer
from django.urls import path
from .token_auth_channels import TokenAuthMiddleware


application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddleware(
        URLRouter([
            path('notification/', NotificationConsumer)
        ]),
    ),
})
