# Generated by Django 2.2 on 2019-05-01 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', help_text='이름', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='임의의 세션', help_text='세션명', max_length=16)),
                ('state', models.CharField(choices=[('READY', '준비'), ('PLAY', '진행중'), ('END', '종료')], default=('READY', '준비'), help_text='상태', max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveSmallIntegerField(default=0, help_text='점수')),
                ('player', models.ForeignKey(help_text='플레이어', on_delete=django.db.models.deletion.CASCADE, to='session.Player')),
                ('session', models.ForeignKey(help_text='세션', on_delete=django.db.models.deletion.CASCADE, to='session.Session')),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(choices=[('DECK', '덱'), ('HAND', '핸드'), ('BOARD', '보드')], default=('DECK', '덱'), help_text='카드의 위치', max_length=8)),
                ('pos_x', models.PositiveSmallIntegerField(blank=True, help_text='보드 위 x 좌표', null=True)),
                ('pos_y', models.PositiveSmallIntegerField(blank=True, help_text='보드 위 y 좌표', null=True)),
                ('pos_z', models.PositiveSmallIntegerField(blank=True, help_text='보드 위 z 좌표', null=True)),
                ('face', models.CharField(blank=True, choices=[('FRONT', '앞면'), ('BACK', '뒷면')], help_text='보드 위 보이는 면', max_length=8, null=True)),
                ('player_session', models.ForeignKey(blank=True, help_text='소유한 플레이어', null=True, on_delete=django.db.models.deletion.CASCADE, to='session.PlayerSession')),
                ('session', models.ForeignKey(help_text='세션', on_delete=django.db.models.deletion.CASCADE, to='session.Session')),
            ],
        ),
    ]