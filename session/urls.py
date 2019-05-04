from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from session import views

urlpatterns = [
    path('', views.intro, name='intro'),
    path('login/', views.login, name='login'),
    path('lobby/', views.lobby, name='lobby'),
    path('create-session/', views.create_session, name='create_session'),
    path('session/<int:session_id>/', views.session, name='session'),
    path('play/', views.play, name='play'),
    path('result/', views.play, name='result'),
]

