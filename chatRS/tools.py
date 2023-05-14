import random
from .utils import rooms, chats
from bson.objectid import ObjectId
import datetime

def check_code(rcode):
    data = rooms.find_one({"_id": rcode})
    if (data == None):
        #room not exists
        return False
    else:
        #room exists
        return data

def get_code():
    l = [chr(x) for x in range(65,91)] + [chr(x) for x in range(97,123)] + [str(x) for x in range(0,10)]
    rcode = "".join(random.sample(l, 6))
    
    while check_code(rcode):
        rcode = "".join(random.sample(l, 6))
    
    return rcode

def join_room(rcode, name):
    if len(rcode) != 6:
        return {"status": "failed", "msg": "Code length must be of 6 digits!"}
    
    data = check_code(rcode)
    if data == False:
        return {"status": "failed", "msg": f"No room exists with code {rcode}!"}
    else:
        if data["status"] == "offline":
            return {"status": "failed", "msg": f"No room exists with code {rcode}!"}
        else:
            if data["door"] == "close":
                return {"status": "failed", "msg": "Room is closed!"}
            else:
                if name == "":
                    name = random.choice(["Tom", "Jerry", "Max", "Mango", "Patato"])
                
                id = ObjectId()
                chats.insert_one({"_id": id, "posted_on": datetime.datetime.now(), "msg":f"{name} joined the room!"})
                data["all_members"].append([id, name])
                data["online_members"].append(id)
                rooms.update_one({"_id": rcode}, data)
                
                return {"status": "success", "msg": "Successfully joined!", "id": id, "name": name}