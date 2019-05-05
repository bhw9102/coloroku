from django.db import models


class CardClass(models.Model):
    color_front = models.CharField(max_length=8, default='#000000', help_text='앞면 색')
    color_back = models.CharField(max_length=8, default='#ffffff', help_text='뒷면 색')
    count = models.PositiveSmallIntegerField(default=5, help_text='카드 수')

