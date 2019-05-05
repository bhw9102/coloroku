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
    player_session_list = PlayerSession.objects.filter(player=player).all()
    for player_session in player_session_list:
        player_session.state = 'EXITED'
        player_session.save()
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
    # GET
    session = Session.objects.filter(pk=session_id).first()
    player = Player.objects.filter(name=request.session['player_name']).first()
    player_session = PlayerSession.objects.filter(player=player, session=session, state='JOINED').first()
    if player_session is None:
        PlayerSession.objects.create(player=player, session=session)
    player_session_list = PlayerSession.objects.filter(session=session, state='JOINED').all()
    return render(request, 'session/room.html', {'player_session_list': player_session_list})


def play(request):
    return render(request, 'session/play.html')


def result(request):
    return render(request, 'session/result.html')


