from rest_framework import serializers
from map.models import Game, GameMembership, GameLog, Map, Tile
from django.contrib.auth.models import User


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'start_date', 'turn_player', 'turn_phase', 'fortifies_used', 'fortifies_remaining')

class TileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tile
        fields = ('map', 'row', 'column', 'units', 'terrain', 'terrain_color', 'owner', 'owner_color', 'border_n', 'border_ne', 'border_nw', 'border_s', 'border_se', 'border_sw', 'highlighted')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
