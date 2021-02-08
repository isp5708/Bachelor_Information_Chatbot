from channels.generic.websocket import AsyncWebsocketConsumer
from . import dialogflowAPI
import os
import json

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "paichaibot-jxekdn-64edeccfdfdf.json"

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        userId = text_data_json['userId']
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'userId': userId,
                'message': message
            }
        )

        if 'chatBot' in message:
            apiAnswer = await dialogflowAPI.getDialogApi(message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_bot_message',
                    'userId': userId,
                    'message': apiAnswer
                }
            )

    # Receive message from room group
    async def chat_bot_message(self, event):
        userId = event['userId']
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chatBot',
            'userId': userId,
            'message': message
        }))

    async def chat_message(self, event):
        userId = event['userId']
        message = event['message']

        await self.send(text_data=json.dumps({
            'type': 'user',
            'userId': userId,
            'message': message
        }))

    
