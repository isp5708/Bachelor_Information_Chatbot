from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:roomName>/<str:userName>/', views.room, name='room'),
]
