from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from session import views

urlpatterns = [
    path('', views.intro, name='intro'),
]