from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from rest_framework import generics, permissions

from django.contrib.auth.models import User
from map.models import Game, GameMembership, GameLog, Map, Tile
from map.serializers import GameSerializer, UserSerializer, TileSerializer
from django.core.serializers.json import DjangoJSONEncoder
import json


def create_map(request):
    rows = 10
    columns = 10
    game = Game.objects.create()
    map = Map.objects.create(game=game)
    game_log = GameLog.objects.create(game=game)
    user = User.objects.get(username='bo')
    GameMembership.objects.create(user=user, game=game)
    for row in range(rows):
        for column in range(columns):
            tile = Tile.objects.create(map=map, row=row, column=column)
            GameLog.objects.create(game=game, action_type="tile_created", tile_effected=tile)

    return render(request, 'create_map.html', {
        'message': "Heyo!",
    })


def game(request, gid):
    game = Game.objects.get(id=gid)
    game_map = Map.objects.get(game=game)
    game_tiles = Tile.objects.filter(map=game_map)
    return render(request, "game.html", {
        'user': request.user,
        'game': game,
        'map': game_map,
        'game_tiles': game_tiles
    })

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'games': reverse('games-list', request=request, format=format)
    })

@csrf_exempt
@login_required
def game_test(request):
    received_json_data = json.loads(request.body)
    data = {}
    data['completed'] = received_json_data['test_var']
    print request.user
    return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def tile_list(request, map_id):
    data = list(Tile.objects.filter(map=map_id))
    json_data = json.dumps(data)
    print json_data
    return HttpResponse(json_data, content_type="application/json")

class GameList(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (permissions.IsAuthenticated,)

class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class TileList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Tile.objects.all()
    serializer_class = TileSerializer

    def get_queryset(self):
        map_id = self.kwargs['map_id']
        return Tile.objects.filter(map=map_id)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer