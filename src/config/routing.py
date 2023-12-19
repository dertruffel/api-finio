from django.urls import path

from config.consumers import NotificationsGetWebsocketConsumer

websocket_urlpatterns = [
    path('ws/notifications/', NotificationsGetWebsocketConsumer.as_asgi()),

]
