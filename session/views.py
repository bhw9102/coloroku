from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from session.form import PlayerForm, SessionForm
from session.models import *
from game.models import CardClass
from session.common import shuffle_ordering


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
    data = dict(player_session_list=player_session_list, session=session)
    return render(request, 'session/room.html', data)


def play(request, session_id):
    session = Session.objects.filter(pk=session_id).first()
    # 세션이 시작 전이라면, 세션 초기화를 한다.
    if session.state == 'READY':
        # 세션 상태를 게임 중으로 변경한다.
        session.state = 'PLAY'
        session.turn = 0
        session.save()
        # 보드판 데이터를 생성한다.
        # TODO: 하드코딩 되어있다.
        board_size = 3
        for x in range(0, board_size):
            for y in range(0, board_size):
                Board.objects.create(session=session, x=x, y=y)
        # 참가자의 게임 순서를 지정한다.
        player_session_list = PlayerSession.objects.filter(session=session, state='JOINED').all()
        for i, player_session in enumerate(player_session_list):
            player_session.order = i
            player_session.save()
        # 게임에 사용될 카드 뭉치를 생성한다.
        card_class_list = CardClass.objects.all()
        for card_class in card_class_list:
            for i in range(5):
                Card.objects.create(session=session, card=card_class)
        # 카드 뭉치를 섞는다.
        card_list = Card.objects.filter(session=session).all()
        ordered = shuffle_ordering(card_list.count())
        for i, card in enumerate(card_list):
            card.order = ordered[i]
            card.save()
        # 첫 핸드를 참가자에게 나눠준다.
        card_list = Card.objects.filter(session=session).order_by('order').all()
        player_cnt = player_session_list.count()
        for player_session in player_session_list:
            p_order = player_session.order
            hand_order_list = [p_order, p_order+player_cnt, p_order+player_cnt*2]
            for hand_order in hand_order_list:
                order_card = card_list.get(order=hand_order)
                order_card.player_session = player_session
                order_card.location = 'HAND'
                order_card.save()
    # 플레이어에게 전달할 게임 진행 정보를 취합한다.
    if session.state == 'PLAY':
        player_session_list = PlayerSession.objects.filter(session=session, state='JOINED').all()
        player_session = PlayerSession.objects.filter(session=session, player__name=request.session['player_name'],
                                                      state='JOINED').first()
        deck_cnt = Card.objects.filter(session=session, location='DECK').all().count()
        hand_list = Card.objects.filter(session=session, location='HAND', player_session=player_session).all()
        board_list = Board.two_dimension_board_list(session=session)
        data = dict(session=session, player_session_list=player_session_list, player_session=player_session,
                    deck_cnt=deck_cnt, hand_list=hand_list, board_list=board_list)
        return render(request, 'session/play.html', data)
    if session.state == 'END':
        return HttpResponseRedirect(reverse('result', kwargs={'session_id': session_id}))
    return render(request, 'session/play.html')


@csrf_exempt
def play_hand(request, session_id):
    if request.method == 'POST':
        # 핸드에 있던 카드를 보드에 놓다.
        card = Card.objects.filter(pk=request.POST['card']).first()
        face = request.POST['face']
        board = Board.objects.filter(pk=request.POST['board']).first()
        card.board = board
        card.face = face
        card.location = 'BOARD'
        card.pos_z = 0
        if board.top_card:
            card.pos_z = board.top_card.pos_z + 1
        card.save()

        # 플레이어는 새로운 카드를 드로우한다.
        player_session = PlayerSession.objects\
            .filter(player__name=request.POST['player_name'], session=session_id).first()
        draw_card = Card.deck_top(session=session_id)
        if draw_card:
            draw_card.location = 'HAND'
            draw_card.player_session = player_session
            draw_card.save()

        # 점수를 계산한다. 핸드에서 카드를 플레이하면, 10점을 준다.
        board_top = Board.objects.filter(session=session_id, x=board.x, y=board.y - 1).first()
        if board_top and board_top.top_card:
            if board_top.top_card.face_card == board.top_card.face_card:
                player_session.score = player_session.score + 10
        board_bottom = Board.objects.filter(session=session_id, x=board.x, y=board.y + 1).first()
        if board_bottom and board_bottom.top_card:
            if board_bottom.top_card.face_card == board.top_card.face_card:
                player_session.score = player_session.score + 10
        board_left = Board.objects.filter(session=session_id, x=board.x - 1, y=board.y).first()
        if board_left and board_left.top_card:
            if board_left.top_card.face_card == board.top_card.face_card:
                player_session.score = player_session.score + 10
        board_right = Board.objects.filter(session=session_id, x=board.x + 1, y=board.y).first()
        if board_right and board_right.top_card:
            if board_right.top_card.face_card == board.top_card.face_card:
                player_session.score = player_session.score + 10
        player_session.save()

        # 순서를 넘기다.
        session = Session.objects.filter(pk=session_id).first()
        session.turn = session.turn + 1

        # 모든 카드가 보드에 놓이면 게임이 종료된다.
        hand_card_list = Card.objects.filter(session=session, location='HAND').all()
        deck_card_list = Card.objects.filter(session=session, location='DECK').all()
        if (hand_card_list.count() == 0) and (deck_card_list.count() == 0):
            session.state = 'END'
        session.save()
        return HttpResponseRedirect(reverse('play', kwargs={'session_id': session_id}))
    return HttpResponseRedirect(reverse('lobby'))


@csrf_exempt
def play_board(request, session_id):
    if request.method == 'POST':
        # 보드에 있던 카드를 뒤집어 다른 보드에 놓다.
        board_prev = Board.objects.filter(pk=request.POST['board_prev']).first()
        board_next = Board.objects.filter(pk=request.POST['board_next']).first()
        card = board_prev.top_card
        card.board = board_next
        if card.face == 'FRONT':
            card.face = 'BACK'
        else:
            card.face = 'FRONT'
        card.pos_z = 0
        if board_next.top_card:
            card.pos_z = board_next.top_card.pos_z + 1
        card.save()

        # 점수를 계산하다. 보드에서 카드를 움직이는 플레이는 20점을 준다.
        player_session = PlayerSession.objects.filter(session=session_id, player__name=request.POST['player_name']).first()
        board_top = Board.objects.filter(session=session_id, x=board_next.x, y=board_next.y-1).first()
        if board_top and board_top.top_card:
            if board_top.top_card.face_card == board_next.top_card.face_card:
                player_session.score = player_session.score + 30
        board_bottom = Board.objects.filter(session=session_id, x=board_next.x, y=board_next.y+1).first()
        if board_bottom and board_bottom.top_card:
            if board_bottom.top_card.face_card == board_next.top_card.face_card:
                player_session.score = player_session.score + 30
        board_left = Board.objects.filter(session=session_id, x=board_next.x-1, y=board_next.y).first()
        if board_left and board_left.top_card:
            if board_left.top_card.face_card == board_next.top_card.face_card:
                player_session.score = player_session.score + 30
        board_right = Board.objects.filter(session=session_id, x=board_next.x+1, y=board_next.y).first()
        if board_right and board_right.top_card:
            if board_right.top_card.face_card == board_next.top_card.face_card:
                player_session.score = player_session.score + 30
        player_session.save()

        # 순서를 넘기다.
        session = Session.objects.filter(pk=session_id).first()
        session.turn = session.turn + 1
        session.save()
        return HttpResponseRedirect(reverse('play', kwargs={'session_id': session_id}))
    return HttpResponseRedirect(reverse('lobby'))


def result(request, session_id):
    player_session_list = PlayerSession.objects.filter(session=session_id).all()
    data = dict(player_session_list=player_session_list)
    return render(request, 'session/result.html', data)


