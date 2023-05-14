from ..utils import rooms, chats

def create_room(data):
    rooms.insert_one(data)

def insert_chat(data):
    chats.insert_one(data)
