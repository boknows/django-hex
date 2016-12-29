from __future__ import unicode_literals

import datetime
from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.db.models import ForeignKey, DecimalField, CharField, IntegerField, BooleanField, EmailField


MAX_PLAYERS_TO_INVITE = 7 # This is NOT including the starting player

class Game(TimeStampedModel):
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(null=True, blank=True)
    turn_player = CharField(max_length=64, null=True, blank=True)
    fortifies_used = IntegerField(null=True, blank=True)
    fortifies_remaining = IntegerField(null=True, blank=True)
    INVITE = 'invite_phase'
    PLAYING = 'playing'
    ENDED = 'ended'
    STATUS_TYPE_CHOICES = (
        (INVITE, 'Player invite phase'),
        (PLAYING, 'Game is in session'),
        (ENDED, 'Game has ended')
    )
    status = models.CharField(
        max_length=12,
        choices=STATUS_TYPE_CHOICES,
        default=INVITE,
    )

    PLACEMENT = 'unit_placement'
    ATTACK = 'attack'
    FORTIFY = 'fortity'
    TURN_PHASE_CHOICES = (
        (PLACEMENT, 'Unit placement phase'),
        (ATTACK, 'Attack phase'),
        (FORTIFY, 'Unit fortification phase')
    )
    turn_phase = models.CharField(
        max_length=14,
        choices=TURN_PHASE_CHOICES,
        default=PLACEMENT,
    )

    def is_ready_to_start(self):
        memberships = self.memberships()
        all_accepted_or_declined = True
        for membership in memberships:
            if membership.membership_type == 'invited':
                all_accepted_or_declined = False

        return all_accepted_or_declined

    def memberships(self):
        return self.gamemembership_set.filter(game=self)

    def players_accepted(self):
        users = []
        for membership in GameMembership.objects.filter(
                game=self,
                membership_type=GameMembership.ACCEPTED)\
                .select_related('user'):
            users.append(membership.user)
        return users

    def players_invited(self):
        users = []
        for membership in GameMembership.objects.filter(
                game=self,
                membership_type=GameMembership.INVITED):
            if membership.email:
                users.append({"type": "email", "value": membership.email})
            else:
                users.append({"type": "user", "value": membership.user})
        return users

    def players_declined(self):
        users = []
        for membership in GameMembership.objects.filter(
                game=self,
                membership_type=GameMembership.DECLINED):
            if membership.email:
                users.append({"type": "email", "value": membership.email})
            else:
                users.append({"type": "user", "value": membership.user})
        return users

    def __str__(self):
        return 'Game - id: %s' % (self.id)


class GameMembership(TimeStampedModel):
    game = ForeignKey(Game, null=False)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, unique=False, null=True)
    email = EmailField(null=True)
    INVITED = 'invited'
    ACCEPTED = 'accepted'
    DECLINED = 'declined'
    MEMBERSHIP_TYPE_CHOICES = (
        (INVITED, 'Invited to Game'),
        (ACCEPTED, 'Accepted Invite'),
        (DECLINED, 'Declined Invite')
    )
    membership_type = models.CharField(
        max_length=8,
        choices=MEMBERSHIP_TYPE_CHOICES,
        default=INVITED,
    )

    def __str__(self):
        return 'GameMembership - id: %s - type: %s' % (self.id, self.membership_type)

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
    units = IntegerField(null=True, blank=True)
    terrain = CharField(max_length=64, null=True, blank=True, default="grassland")
    terrain_color = CharField(max_length=64, null=True, blank=True, default="green")
    owner = models.ForeignKey(User, unique=False, null=True)
    owner_color = CharField(max_length=64, null=True, blank=True)
    border_n = CharField(max_length=64, null=True, blank=True)
    border_s = CharField(max_length=64, null=True, blank=True)
    border_ne = CharField(max_length=64, null=True, blank=True)
    border_nw = CharField(max_length=64, null=True, blank=True)
    border_se = CharField(max_length=64, null=True, blank=True)
    border_sw = CharField(max_length=64, null=True, blank=True)
    tile_text = CharField(max_length=64, null=True, blank=True)
    highlighted = BooleanField(default=False)

    def __str__(self):
        return 'Tile - row(%s) column(%s) - Owner(%s) - map_id(%s)' % (self.row, self.column, self.owner, self.map.id)

    def attack(self, tile):
        print self, " is attacking ", tile

    def place_units(self):
        pass


class Action(TimeStampedModel):
    MISCELLANEOUS = 'MISC'
    TILE_ASSIGNMENT = 'TA'
    ATTACK = 'ATT'
    PLACEMENT = 'PLACE'
    MOVE = 'MOVE'
    FORTIFY = 'FORT'
    BEGIN_TURN = 'BEGIN'
    END_TURN = 'END'

    ACTION_TYPE_CHOICES = (
        (TILE_ASSIGNMENT, 'Tile Assignment'),
        (MISCELLANEOUS, 'Miscellaneous'),
        (ATTACK, 'Attack'),
        (PLACEMENT, 'Unit Placement'),
        (MOVE, 'Moving Units'),
        (FORTIFY, 'Fortify Unit'),
        (BEGIN_TURN, 'Begin Turn'),
        (END_TURN, 'End Turn'),
    )
    user = models.ForeignKey(User, unique=False, null=True)
    map = ForeignKey(Map, null=False)
    date = models.DateTimeField(null=True, blank=True)
    action_type = models.CharField(
        max_length=5,
        choices=ACTION_TYPE_CHOICES,
        default=MISCELLANEOUS,
    )
    tile_acting = ForeignKey(Tile, related_name='tile_acting', null=True)
    tile_effected = ForeignKey(Tile, related_name='tile_effected', null=True)
    units = IntegerField(null=True, blank=True)
    message = CharField(max_length=200, null=True, blank=True)
