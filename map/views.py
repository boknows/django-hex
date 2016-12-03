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
from map.models import Game, GameMembership, Action, Map, Tile
from map.serializers import GameSerializer, UserSerializer, TileSerializer, ActionSerializer, MapSerializer
from map.forms import InvitedForm
from dashboard.start_game import create_tiles

import json


def create_map(request):
    rows = 10
    columns = 10
    game = Game.objects.create()
    map = Map.objects.create(game=game)
    game_log = Action.objects.create(game=game)
    user = User.objects.get(username='bo')
    GameMembership.objects.create(user=user, game=game)
    for row in range(rows):
        for column in range(columns):
            tile = Tile.objects.create(map=map, row=row, column=column)
            Action.objects.create(game=game, action_type="tile_created", tile_effected=tile)

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

def pre_game(request, gid):
    game = Game.objects.get(id=gid)
    membership = GameMembership.objects.get(game=game, user=request.user)
    if request.method == 'POST':
        form = InvitedForm(instance=membership, data=request.POST, prefix="invited_form")
        if form.is_valid():
            membership = form.save(commit=False)
            membership.save()
            if game.is_ready_to_start():
                create_tiles(game=game)
        else:
            print "not valid"
    else:
        form = InvitedForm(instance=membership, prefix="invited_form")
    return render(request, "pre_game.html", {
        'user': request.user,
        'membership': membership,
        'game': game,
        'form': form
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


class GameList(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (permissions.IsAuthenticated,)

class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class ActionDetail(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Action.objects.all()
    serializer_class = ActionSerializer

    def get_queryset(self):
        map_id = self.kwargs['map_id']
        return Action.objects.filter(map=map_id)

class MapDetail(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Map.objects.all()
    serializer_class = MapSerializer

    def get_queryset(self):
        map_id = self.kwargs['map_id']
        return Map.objects.filter(id=map_id)

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