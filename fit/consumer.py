import imp
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import authenticate, login
from channels.db import database_sync_to_async
import channels
class CommunicationConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = []

    async def connect(self):
        self.roomGroupName = 'fit'
        user=await channels.auth.get_user(self.scope)
        self.user.append(user.id)
        
        
        await self.channel_layer.group_add(
            self.roomGroupName,
           "siva"
        )
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Hi welcome to fita", }))

    async def disconnect(self, close_code):
            print(self.channel_name)
            await self.channel_layer.group_discard(
                self.roomGroupName,
                self.channel_name
            )
            

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            print(type(text_data_json))
            #save the session (if the session backend does not access the db you can use `sync_to_async`)
            #await database_sync_to_async(self.scope["session"].save)()
            await self.channel_layer.group_send(
                self.roomGroupName, {
                    "type": "sendMessage",
                    "message": "hi",
                })
        except Exception as e:
            print(e)

    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(text_data=json.dumps({"message": message, "username": username}))