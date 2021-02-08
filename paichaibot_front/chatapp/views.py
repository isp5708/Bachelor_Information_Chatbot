from django.shortcuts import render
from django.http import HttpResponse
from channels.http import AsgiRequest
# Create your views here.

# chatting
from django.utils.safestring import mark_safe

from . import host_observer

import json
import re

def index(request):
    return render(request, 'chat/index.html', {})

# 정적 변수를 사용하기 위한 decorator
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

@static_vars(observer=host_observer.HostObserver.instance())
def chat(request, room_name):
    pattern = re.compile('^[A-Za-z0-9+]*$')
    
    if pattern.match(room_name) == None:
        return HttpResponse('<script>alert("영소문자, 숫자만 입력 가능합니다."); \
                                     location.href="/";</script>')

    if not chat.observer.add(host=room_name):
        return HttpResponse('<script>alert("다른 이름을 사용하세요."); \
                                     location.href="/";</script>')

    return render(request, 'chat/chat.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })