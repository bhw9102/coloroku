from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from session import views

urlpatterns = [
    path('', views.intro, name='intro'),
    path('login/', views.login, name='login'),
    path('lobby/', views.lobby, name='lobby'),
    path('create-room/', views.create_room, name='create_room'),
    path('room/<int:session_id>/', views.room, name='room'),
    path('play/<int:session_id>/', include([
        path('', views.play, name='play'),
        path('hand/', views.play_hand, name='play_hand'),
        path('board/', views.play_board, name='play_board')
    ])),
    path('result/<int:session_id>/', views.result, name='result'),
]

