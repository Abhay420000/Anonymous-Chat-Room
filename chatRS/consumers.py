import json
#from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from .tools import leave_room, save_chat, check_code
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.rcode = self.scope["url_route"]["kwargs"]["rcode"]
        self.uid = self.scope["url_route"]["kwargs"]["uid"]

        #join the group
        await self.channel_layer.group_add(
            self.rcode, self.channel_name
        )
        
        #security check
        data = await database_sync_to_async(check_code)(self.rcode)
        
        if data == False:
            return
        
        self.name = ""
        for all_members in data["all_members"]:
            if str(all_members[0]) == self.uid:
                self.name = all_members[1]
                break
        
        if self.name == "":
            return
        
        await self.accept()
        
        #sending join message to others
        await self.channel_layer.group_send(
                self.rcode, {"type": "join_message", "uid": self.uid, "name": self.name}
            )

    async def disconnect(self, close_code):
        # Leave the room - Authorized Person
        if (close_code != 400):
            await database_sync_to_async(leave_room)(self.uid, self.rcode)
            
            #Send a leave message to all other members
            await self.channel_layer.group_send(
                self.rcode, {"type": "leave_message", "uid": self.uid, "name": self.name}
            )
        
        # Leave the room - UnAuthorized Person
        await self.channel_layer.group_discard(
            self.rcode, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        msg = text_data_json["msg"]
        name = text_data_json["name"]
        
        # Invalid uid
        if (self.uid != text_data_json["uid"]):
            # Disconnect the invalid user
            self.disconnect(400)
            
        # Save messages to database
        s = await database_sync_to_async(save_chat)(self.uid, self.rcode, msg)
        if (s == "error"):
            # Disconnect the invalid user
            self.disconnect(400)
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.rcode, {"type": "chat_message", "name": name, "msg": msg, "uid": self.uid}
        )
    
    # Receive message from room group
    async def chat_message(self, event):
        uid = event["uid"]
        if (uid != self.uid):
            # Send message to WebSocket
            await self.send(text_data=json.dumps(event))
    
    async def join_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))
    
    async def leave_message(self, event):
        uid = event["uid"]
        if (uid != self.uid):
            # Send message to WebSocket
            await self.send(text_data=json.dumps(event))