from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe # json 파싱 라이브러리
import json

# Create your views here.
def index(request):
    return render(request,'welcome/index.html',{})
    #html="<html><body>하위!</body></html>"
    #return HttpResponse(html)

def test(request):
    html="test" 
    return HttpResponse(html)

def room(request,roomName,userName):
    return render(request,'welcome/room.html',{
        'room_name_json' :mark_safe(json.dumps(roomName)),
        'user_name_json' :mark_safe(json.dumps(userName)),
    })


