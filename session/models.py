from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=32, default='', help_text='이름')


SESSION_STATE = (
    ('READY', '준비'),
    ('PLAY', '진행중'),
    ('END', '종료')
)


class Session(models.Model):
    name = models.CharField(max_length=16, default='임의의 세션', help_text="세션명")
    state = models.CharField(max_length=8, choices=SESSION_STATE, default=SESSION_STATE[0], help_text='상태')


class PlayerSession(models.Model):
    player = models.ForeignKey('Player', on_delete=models.CASCADE, help_text='플레이어')
    session = models.ForeignKey('Session', on_delete=models.CASCADE, help_text='세션')
    score = models.PositiveSmallIntegerField(default=0, help_text='점수')


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
    location = models.CharField(max_length=8, choices=CARD_LOCATION, default=CARD_LOCATION[0], help_text='카드의 위치')
    player_session = models.ForeignKey('PlayerSession', null=True, blank=True, on_delete=models.CASCADE, help_text='소유한 플레이어')
    pos_x = models.PositiveSmallIntegerField(null=True, blank=True, help_text='보드 위 x 좌표')
    pos_y = models.PositiveSmallIntegerField(null=True, blank=True, help_text='보드 위 y 좌표')
    pos_z = models.PositiveSmallIntegerField(null=True, blank=True, help_text='보드 위 z 좌표')
    face = models.CharField(max_length=8, choices=CARD_FACE, null=True, blank=True, help_text='보드 위 보이는 면')




