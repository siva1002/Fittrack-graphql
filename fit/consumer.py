import imp
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import authenticate, login
from channels.db import database_sync_to_async
import channels
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
class CommunicationConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = []

    async def connect(self):
        self.roomGroupName = self.scope['url_route']['kwargs']['id']
        user=await channels.auth.get_user(self.scope)
        self.user.append(user.id)
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({"message": f"Hi welcome to fitrack {self.roomGroupName}", }))

    async def disconnect(self, close_code):
            await self.channel_layer.group_discard(
                self.roomGroupName,
                self.channel_name
            )
            

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            to=text_data_json['to']
            print(text_data_json)
            #save the session (if the session backend does not access the db you can use `sync_to_async`)
            #await database_sync_to_async(self.scope["session"].save)()
            await self.channel_layer.group_send(
                str(to), {
                    "type": "sendMessage",
                    "message": text_data_json['message'],
                })
        except Exception as e:
            print(e)

    async def sendMessage(self, event):
        await self.send(text_data=json.dumps({"message": event['message']}))