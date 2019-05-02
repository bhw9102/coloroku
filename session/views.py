from django.shortcuts import render


def intro(request):
    return render(request, 'session/intro.html')


def login(request):
    return render(request, 'session/login.html')


def lobby(request):
    return render(request, 'session/intro.html')


def create_room(request):
    return render(request, 'session/intro.html')


def room(request):
    return render(request, 'session/intro.html')


def play(request):
    return render(request, 'session/intro.html')


def result(request):
    return render(request, 'session/intro.html')


