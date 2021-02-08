from django.urls import path
from . import views

urlpatterns = [
   
    path('',views.index,name='index'),
    path('<str:roomName>/<str:userName>/',views.room,name='room'), # string이 오면 넣어준다 roomName 이라는 변수를 ... 
]