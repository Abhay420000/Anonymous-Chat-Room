import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .tools import leave_room

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        
        self.rcode = self.scope["url_route"]["kwargs"]["rcode"]
        self.uid = self.scope["url_route"]["kwargs"]["uid"]
        
        #join the group
        async_to_sync(self.channel_layer.group_add)(
            self.rcode, self.channel_name
        )
        
        #Check if User is valid
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.rcode, self.channel_name
        )
        
        leave_room(self.uid, self.rcode)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        msg = text_data_json["msg"]
        name = text_data_json["name"]
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.rcode, {"name": name, "msg": msg}
        )
    
    # Receive message from room group
    def chat_message(self, event):
        name = event["name"]
        msg = event["msg"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"name": name, "msg": msg}))