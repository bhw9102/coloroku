from django.db import models
from django.db.models import Max

class Player(models.Model):
    name = models.CharField(max_length=32, help_text='이름')

    def __str__(self):
        return self.name


SESSION_STATE = (
    ('READY', '준비'),
    ('PLAY', '진행중'),
    ('END', '종료')
)


class Session(models.Model):
    name = models.CharField(max_length=16, null=False, blank=False, default='임의의 세션', help_text='세션명')
    state = models.CharField(max_length=8, null=False, blank=True, choices=SESSION_STATE, default='READY', help_text='상태')
    turn = models.PositiveSmallIntegerField(default=0, null=True, blank=True, help_text='현재 턴 수, 0부터 시작')

    def __str__(self):
        return "{}-{}".format(self.name, self.state)

    @property
    def player_cnt(self):
        return PlayerSession.objects.filter(session=self, state='JOINED').all().count()


JOINED_STATE = (
    ('JOINED', '참여한'),
    ('EXITED', '퇴장한'),
)


class PlayerSession(models.Model):
    player = models.ForeignKey('Player', on_delete=models.CASCADE, help_text='플레이어')
    session = models.ForeignKey('Session', on_delete=models.CASCADE, help_text='세션')
    score = models.PositiveSmallIntegerField(default=0, help_text='점수')
    state = models.CharField(max_length=8, null=False, blank=True, choices=JOINED_STATE, default='JOINED', help_text='참여 상태')
    order = models.PositiveSmallIntegerField(null=True, blank=True, help_text='순서, 0부터 시작')

    def __str__(self):
        return '{}-{}'.format(self.player, self.session)

    @property
    def is_turn(self):
        turn = self.session.turn
        player_cnt = self.session.player_cnt
        current_order = turn % player_cnt
        return self.order is current_order


CARD_LOCATION = (
    ('DECK', '덱'),
    ('HAND', '핸드'),
    ('BOARD', '보드')
)

CARD_FACE = (
    ('FRONT', '앞면'),
    ('BACK', '뒷면')
)


class Card(models.Model):
    session = models.ForeignKey('Session', on_delete=models.CASCADE, help_text='세션')
    card = models.ForeignKey('game.CardClass', on_delete=models.CASCADE, help_text='카드')
    location = models.CharField(max_length=8, choices=CARD_LOCATION, default='DECK', help_text='카드의 위치')
    order = models.PositiveSmallIntegerField(null=True, blank=True, help_text='카드 뭉치 속에서 순서, 0부터 가장 위')
    player_session = models.ForeignKey('PlayerSession', null=True, blank=True, on_delete=models.CASCADE, help_text='소유한 플레이어')
    board = models.ForeignKey('Board', null=True, blank=True, on_delete=models.CASCADE)
    pos_z = models.PositiveSmallIntegerField(null=True, blank=True, help_text='보드 위 z 좌표')
    face = models.CharField(max_length=8, choices=CARD_FACE, null=True, blank=True, default='FRONT', help_text='보드 위 보이는 면')

    @property
    def face_card(self):
        if self.face == 'FRONT':
            return self.card.color_front
        # elif self.face == 'BACK'
        return self.card.color_back


class Board(models.Model):
    session = models.ForeignKey('Session', on_delete=models.CASCADE, help_text='세션')
    x = models.PositiveSmallIntegerField(help_text='보드 위 x 좌표')
    y = models.PositiveSmallIntegerField(help_text='보드 위 y 좌표')

    def __str__(self):
        return '{}-({},{})'.format(self.session, self.x, self.y)

    @property
    def top_card(self):
        card_list = Card.objects.filter(location='BOARD', board=self).all()
        card = Card.objects.filter(location='BOARD', board=self).first()
        for tmp in card_list:
            if card.pos_z < tmp.pos_z:
                card = tmp
        return card
        # return self.card_set.all().aggregate(models.Max('pos_z'))

    @classmethod
    def two_dimension_board_list(cls, session):
        # TODO: 하드코딩 되어있다.
        board_size = 3
        board_list = list()
        for y in range(0, board_size):
            column_list = list()
            for x in range(0, board_size):
                board = Board.objects.filter(session=session, x=x, y=y).first()
                column_list.append(board)
            board_list.append(column_list)
        return board_list





