from django.urls import path
from .consumers import StockConsumer

websocket_urlpatterns = [
    path("ws/stock_updates/", StockConsumer.as_asgi()),
]
