from rest_framework import serializers
from map.models import Game, GameMembership, GameLog, Map, Tile
from django.contrib.auth.models import User


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('id', 'start_date', 'turn_player', 'turn_phase', 'fortifies_used', 'fortifies_remaining')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
