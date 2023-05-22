import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .tools import leave_room, save_chat

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        
        self.rcode = self.scope["url_route"]["kwargs"]["rcode"]
        self.uid = self.scope["url_route"]["kwargs"]["uid"]

        print(self.rcode, self.channel_name)
        #join the group
        async_to_sync(self.channel_layer.group_add)(
            self.rcode, self.channel_name
        )
        
        #Check if User is valid
        self.accept()

    def disconnect(self, close_code):
        # Leave the room - Authorized Person
        if (close_code != 400):
            leave_room(self.uid, self.rcode)
            
            #Send a leave message to all other members
            async_to_sync(self.channel_layer.group_send)(
                self.rcode, {"type": "leave_message", "uid": self.uid}
            )
        
        # Leave the room - UnAuthorized Person
        async_to_sync(self.channel_layer.group_discard)(
            self.rcode, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        msg = text_data_json["msg"]
        name = text_data_json["name"]
        
        # Save messages to database
        s = save_chat(self.uid, self.rcode, msg)
        if (s == "error"):
            # Disconnect the invalid user
            self.disconnect(400)
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.rcode, {"type": "chat_message", "name": name, "msg": msg, "uid": self.uid}
        )
    
    # Receive message from room group
    def chat_message(self, event):
        uid = event["uid"]
        if (uid != self.uid):
            # Send message to WebSocket
            if (event["type"] == "chat_message"):
                    self.send(text_data=json.dumps(event))
    
    def leave_message(self, event):
        uid = event["uid"]
        if (uid != self.uid):
            # Send message to WebSocket
            if (event["type"] == "leave_message"):
                    self.send(text_data=json.dumps(event))