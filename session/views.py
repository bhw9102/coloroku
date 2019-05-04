from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from session.form import PlayerForm
from session.models import *


def intro(request):
    return render(request, 'session/intro.html')


def login(request):
    # POST
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            player = Player.objects.filter(name=name).first()
            if player is None:
                player = Player.objects.create(name=name)
            request.session['player_name'] = player.name
            return HttpResponseRedirect(reverse('lobby'))
    # GET
    request.session['player_name'] = "test"
    player_form = PlayerForm(initial={"name":""})
    return render(request, 'session/login.html', {'player_form': player_form})


def lobby(request):
    print("test1 : ", request.session['player_name'])
    player = Player.objects.filter(name=request.session.get('player_name')).first()
    print("test1 : ", player)
    return render(request, 'session/intro.html')


def create_room(request):
    return render(request, 'session/intro.html')


def room(request):
    return render(request, 'session/intro.html')


def play(request):
    return render(request, 'session/intro.html')


def result(request):
    return render(request, 'session/intro.html')


