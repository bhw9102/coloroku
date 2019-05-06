from django.db import models


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
    pos_x = models.PositiveSmallIntegerField(null=True, blank=True, help_text='보드 위 x 좌표')
    pos_y = models.PositiveSmallIntegerField(null=True, blank=True, help_text='보드 위 y 좌표')
    pos_z = models.PositiveSmallIntegerField(null=True, blank=True, help_text='보드 위 z 좌표, 보이는 카드의 값이 0이 되도록 한다.')
    face = models.CharField(max_length=8, choices=CARD_FACE, null=True, blank=True, default='FRONT', help_text='보드 위 보이는 면')




