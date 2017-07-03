from rest_framework import serializers
from map.models import Game, GameMembership, Action, Tile
from django.contrib.auth.models import User


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'start_date', 'turn_player', 'turn_phase', 'fortifies_used', 'fortifies_remaining', 'rows', 'columns')
        lookup_field = 'id'

class TileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tile
        fields = ('id', 'game_id', 'row', 'column', 'units', 'terrain', 'terrain_color', 'owner', 'owner_color', 'border_n', 'border_ne', 'border_nw', 'border_s', 'border_se', 'border_sw', 'highlighted')

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('id', 'user', 'tile_acting', 'tile_effected', 'game', 'action_type', 'units')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


