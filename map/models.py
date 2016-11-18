from __future__ import unicode_literals

import datetime
from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.db.models import ForeignKey, DecimalField, CharField, IntegerField
from django.utils.encoding import python_2_unicode_compatible


MAX_PLAYERS_TO_INVITE = 7 # This is NOT including the starting player

class Game(TimeStampedModel):
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(null=True, blank=True)
    turn_player = CharField(max_length=64, null=True, blank=True)
    turn_phase = CharField(max_length=64, null=True, blank=True)
    fortifies_used = IntegerField(null=True, blank=True)
    fortifies_remaining = IntegerField(null=True, blank=True)

    def players(self):
        users = []
        print self
        memberships = self.gamemembership_set.all()
        print memberships
        for membership in memberships:
            if membership.user not in users:
                users.append(membership.user)
        return users

    def __str__(self):
        return 'Game - id: %s' % (self.id)


class GameMembership(TimeStampedModel):
    game = ForeignKey(Game, null=False)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, unique=False)


class Map(TimeStampedModel):
    game = ForeignKey(Game, null=False)
    radius = DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    height = DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    width = DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    side = DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    rows = IntegerField(null=True, blank=True)
    columns = IntegerField(null=True, blank=True)

class Tile(TimeStampedModel):
    map = ForeignKey(Map, null=False)
    row = IntegerField(null=True, blank=True)
    column = IntegerField(null=True, blank=True)
    terrain = CharField(max_length=64, null=True, blank=True)
    terrain_color = CharField(max_length=64, null=True, blank=True)
    owner = models.ForeignKey(User, unique=False, null=True)
    onwer_color = CharField(max_length=64, null=True, blank=True)
    border_n = CharField(max_length=64, null=True, blank=True)
    border_s = CharField(max_length=64, null=True, blank=True)
    border_ne = CharField(max_length=64, null=True, blank=True)
    border_nw = CharField(max_length=64, null=True, blank=True)
    border_se = CharField(max_length=64, null=True, blank=True)
    border_sw = CharField(max_length=64, null=True, blank=True)
    tile_text = CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return 'Tile - row(%s) column(%s) - Owner(%s) - map_id(%s)' % (self.row, self.column, self.owner, self.map.id)


class GameLog(TimeStampedModel):
    MISCELLANEOUS = 'MISC'
    TILE_ASSIGNMENT = 'TA'
    ATTACK = 'ATT'
    PLACEMENT = 'PL'
    FORTIFY = 'FORT'
    BEGIN_TURN = 'BEGN'
    END_TURN = 'END'

    ACTION_TYPE_CHOICES = (
        (TILE_ASSIGNMENT, 'Tile Assignment'),
        (MISCELLANEOUS, 'Miscellaneous')
    )

    game = ForeignKey(Game, null=False)
    date = models.DateTimeField(null=True, blank=True)
    action_type = models.CharField(
        max_length=4,
        choices=ACTION_TYPE_CHOICES,
        default=MISCELLANEOUS,
    )
    tile_acting = ForeignKey(related_name='tile_acting', to='Tile', null=True),
    tile_effected = ForeignKey(related_name='tile_effected', to='Tile', null=True)
    message = CharField(max_length=200, null=True, blank=True)
