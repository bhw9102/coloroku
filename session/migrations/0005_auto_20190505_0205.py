# Generated by Django 2.2 on 2019-05-05 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0004_playersession_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='playersession',
            name='order',
            field=models.PositiveSmallIntegerField(blank=True, help_text='순서, 0부터 시작', null=True),
        ),
        migrations.AddField(
            model_name='session',
            name='turn',
            field=models.PositiveSmallIntegerField(blank=True, default=0, help_text='현재 턴 수, 0부터 시작', null=True),
        ),
    ]
