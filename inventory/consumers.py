import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Product
from asgiref.sync import sync_to_async

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("stock_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("stock_updates", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        product_id = data.get("product_id")

        # Fetch updated stock info
        product = await sync_to_async(Product.objects.get)(id=product_id)
        updated_stock = product.quantity_in_stock

        # Send update to WebSocket group
        await self.channel_layer.group_send(
            "stock_updates",
            {
                "type": "stock_update",
                "product_id": product_id,
                "updated_stock": updated_stock,
            },
        )

    async def stock_update(self, event):
        await self.send(text_data=json.dumps({
            "product_id": event["product_id"],
            "updated_stock": event["updated_stock"],
        }))
