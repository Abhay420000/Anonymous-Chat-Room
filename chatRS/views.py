from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.

"""
sudo
{
    room_code: str,
    language: str,
    countary: str,
    max_room_size: int,
    online_members: int,
    room_admins: Array of str,
    members: Array of str,
    chats:Array of docs,
}

sample data of storage:
{
    room_code: '12XF4',
    
    language: 'English',
    
    countary: 'India',
    
    max_room_size: 10,
    
    online_members: 3,
    
    room_admins: [
        'Abhay',
        ],
    
    members: [
        'Abhay', 
        'Rohan', 
        'Aman'
        ],
    
    chats: [
        {'Abhay':'HI!'}, 
        {'Rohan': 'hi, abhay'},
        {'HOST': 'Aman joined the chat room!'},
        {'Abhay': 'hello aman!'},
        ],
}
"""
@ensure_csrf_cookie
def home(request):
    print(request)
    
    if request.method == "GET":
        return render(request, 'chatRS/index.html')
    elif request.method == "POST":
        print(request)
        return HttpResponse("OK")
    
    return HttpResponse("ERROR")