import json

from channels.generic.websocket import AsyncWebsocketConsumer




class NotificationsGetWebsocketConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        try:
            user = self.scope['user']
        except Exception as e:
            print(e)
            return await self.send(text_data=json.dumps({'error': 'You are not logged in'}))
        await self.accept()
        await self.channel_layer.group_add(
            "notifications",
            self.channel_name
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "notifications",
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        print("user asked for notifcation:",self.scope['user'])
        # /ws/notifications/?token=
        #           {"action": "subscribe_instance", "pk": 1, "request_id": 1}

        try:
            if self.scope['user'].is_anonymous:
                return await self.send(text_data=json.dumps({'error': 'You are not logged in', 'user': f"{self.scope['user']}"}))

            await self.send(text_data='')
        except Exception as e:
            print(e)
            await self.send(text_data=json.dumps({'error': 'Something went wrong'}))
