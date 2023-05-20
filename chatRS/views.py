from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
import json
from .tools import join_room, create_room, leave_room

#@ensure_csrf_cookie
@csrf_exempt
def home(request):
    print(request.body)
    
    if request.method == "GET":
        return render(request, 'chatRS/index.html')
    
    elif request.method == "POST":
        c_req = json.loads(request.body.decode('utf-8'))
        
        to_send = {}
        
        if (c_req["action"] == "create room"):
            rcode = create_room(c_req["max_room_size"])
            to_send = join_room(rcode, c_req["name"])
            
        elif (c_req["action"] == "join room"):
            to_send = join_room(c_req["room_code"], c_req["name"])
        
        elif (c_req["action"] == "leave room"):
            to_send = leave_room(c_req["id"])
        
        to_send =  json.dumps(to_send)
        return HttpResponse(to_send, content_type="application/json")
    
    return HttpResponse("ERROR")