# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-01 21:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0018_auto_20161130_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='status',
            field=models.CharField(choices=[('invite_phase', 'Player invite phase'), ('playing', 'Game is in session'), ('ended', 'Game has ended')], default='invite_phase', max_length=12),
        ),
    ]
