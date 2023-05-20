import random
from .utils import rooms, chats
from bson.objectid import ObjectId
import datetime

def check_code(rcode):
    #Check if room exists. If exists return data
    data = rooms.find_one({"_id": rcode})
    if (data == None):
        #room not exists
        return False
    else:
        #room exists
        return data

def get_code():
    #Generate a new room code
    l = [chr(x) for x in range(65,91)] + [chr(x) for x in range(97,123)] + [str(x) for x in range(0,10)]
    rcode = "".join(random.sample(l, 6))
    
    while check_code(rcode):
        rcode = "".join(random.sample(l, 6))
    
    return rcode

def join_room(rcode, name):
    
    #Invalid Room Code
    if len(rcode) != 6:
        return {"status": "failed", "msg": "Code length must be of 6 digits!"}
    
    data = check_code(rcode)
    #No room exists
    if data == False:
        return {"status": "failed", "msg": f"No room exists with code {rcode}!"}
    else:
        #Room is closed
        if data["status"] == "offline":
            return {"status": "failed", "msg": f"No room exists with code {rcode}!"}
        else:
            #Room is closed
            if data["door"] == "close":
                return {"status": "failed", "msg": "Room is closed!"}
            else:
                #Room is full
                if data["max_room_size"] == data["current_room_size"]:
                    return {"status": "failed", "msg": "Room is full!"}
                
                #Joined Success
                if name == "":
                    name = random.choice(["Tom", "Jerry", "Max", "Mango", "Patato"])
                id = ObjectId()
                chats.insert_one({
                    "_id": id, 
                    "posted_on": datetime.datetime.now(), 
                    "msg":f"{name} joined the room!",
                })
                rooms.update_one(
                    {"_id": rcode}, 
                    {
                        "$push": {"all_members": [id, name], "online_members": id}, 
                        "$inc": {"current_room_size": 1}
                    }, 
                    upsert=False
                )
                return {"room_code": rcode, "status": "success", "msg": "Successfully joined!", "id": str(id), "name": name}

def create_room(max_room_size):
    rcode = get_code()
    rooms.insert_one({
        "_id": rcode,
        "status": "online",
        "door": "open",
        "max_room_size": int(max_room_size),
        "current_room_size": 0,
        "created_on": datetime.datetime.now(),
        "online_members": [],
        "all_members": [],
    })
    return rcode

def leave_room(id, rcode):
    
    #check if room exists
    data = check_code(rcode)
    print(data)
    if (data == False):
        return {"msg": "failed"}
    else:
        for members in data["online_members"]:
            #Check if request is valid
            if members == id:
                rooms.update_one(
                    {"_id":rcode}, 
                    {
                        "$pull":{"online_members":ObjectId(id)},
                        "$inc":{"current_room_size":-1}
                    }
                )
                return {"msg": "success"}
            else:
                return {"msg": "failed"}