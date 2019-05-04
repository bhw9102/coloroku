from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from session.form import PlayerForm, SessionForm
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
    player_form = PlayerForm(initial={"name":""})
    return render(request, 'session/login.html', {'player_form': player_form})


def lobby(request):
    player = Player.objects.filter(name=request.session['player_name']).first()
    # GET
    # TODO: 접속해있던 모든 방에서 나가지게 해야한다.
    session_list = Session.objects.filter(state="READY").all()
    return render(request, 'session/lobby.html', {'session_list': session_list})


def create_room(request):
    # POST
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            session = Session.objects.create(name=name)
            request['session'] = session
            return HttpResponseRedirect(reverse('room', kwargs={'session_id': session.id}))
    # GET
    return render(request, 'session/create_room.html')


def room(request, session_id):

    return render(request, 'session/room.html')


def play(request):
    return render(request, 'session/play.html')


def result(request):
    return render(request, 'session/result.html')


