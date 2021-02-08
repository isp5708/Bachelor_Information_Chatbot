from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

# Create your views here.

def index(request):
    # html = "<html><body>안녕하세요</body></html>"
    # return HttpResponse(html)

    return render(request,'welcome/index.html',{})

def room(request, roomName, userName):
    return render(request,'welcome/room.html',{
        'room_name_json' : mark_safe(json.dumps(roomName)),
        'user_name_json' : mark_safe(json.dumps(userName)),
    })
