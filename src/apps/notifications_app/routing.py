from django.urls import path
from .consumers import NotificationConsumer


websocket_urlpatterns = [
    path(
        "ws/notifs",
        NotificationConsumer.as_asgi(),
        name="websocket-notif",
    )
]
