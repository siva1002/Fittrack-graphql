from django.urls import path , include
from .consumer import CommunicationConsumer

websocket_urlpatterns = [
	path(r'ws/join/fit/<str:id>' , CommunicationConsumer.as_asgi()),
    # path(r'ws/send/<str>') 
]