# Generated by Django 2.2 on 2019-05-05 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardclass',
            name='count',
            field=models.PositiveSmallIntegerField(default=5, help_text='카드 수'),
        ),
    ]
