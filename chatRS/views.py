from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from .tools import get_code, check_code, join_room

@ensure_csrf_cookie
def home(request):
    print(request)
    
    if request.method == "GET":
        return render(request, 'chatRS/index.html')
    
    elif request.method == "POST":
        c_req = json.loads(request.body.decode('utf-8'))
        
        to_send = {}
        
        if (c_req["action"] == "create room"):
            to_send = {"room_code": get_code(), "name": "Unknown"}
            
        elif (c_req["action"] == "join room"):
            to_send = join_room(c_req["room_code"], c_req["name"])
        
        to_send =  json.dumps(to_send)
        return HttpResponse(to_send, content_type="application/json")
    
    return HttpResponse("ERROR")