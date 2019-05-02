from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from session import views

urlpatterns = [
    path('', views.intro, name='intro'),
    path('login/', views.login, name='login'),
    path('lobby/', views.lobby, name='lobby'),
    path('create-room/', views.create_room, name='create_room'),
    path('room/', views.room, name='room'),
    path('play/', views.play, name='play'),
    path('result/', views.play, name='result'),
]

