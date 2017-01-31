from pprint import pprint

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions, mixins
from django.contrib.auth.models import User
from map.models import Game, GameMembership, Action, Map, Tile
from map.serializers import GameSerializer, UserSerializer, TileSerializer, ActionSerializer, MapSerializer
from map.forms import InvitedForm
from dashboard.start_game import create_tiles
from actions import attack, move
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

    return render(request, 'map/create_map.html', {
        'message': "Heyo!",
    })


def game(request, gid):
    game = Game.objects.get(id=gid)
    game_map = Map.objects.get(game=game)
    game_tiles = Tile.objects.filter(map=game_map)
    return render(request, "map/game.html", {
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
    return render(request, "map/pre_game.html", {
        'user': request.user,
        'membership': membership,
        'game': game,
        'form': form
    })

@csrf_exempt
@login_required
def game_test(request):
    received_json_data = json.loads(request.body)
    data = {}
    data['completed'] = received_json_data['test_var']
    print request.user
    return HttpResponse(json.dumps(data), content_type="application/json")


@api_view(['GET', 'POST'])
def action_detail(request):
    if request.method == 'POST':
        serializer = ActionSerializer(data=request.data)

        if serializer.is_valid():
            tile_acting = serializer.validated_data['tile_acting']
            tile_effected = serializer.validated_data['tile_effected']
            map = serializer.validated_data['map']
            action_type = serializer.validated_data['action_type']
            # Validation rules for suspicious calls
            if tile_acting.owner != request.user:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if tile_acting.map != map or tile_effected.map != map:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if action_type == "ATT":
                tile_acting, tile_effected = attack(map, tile_acting, tile_effected)
                # if tile_effected.tiles == 0, prompt for movement action details on UI
            if action_type == "MOVE":
                units_to_move = serializer.validated_data['units']
                tile_acting, tile_effected = move(map, tile_acting, tile_effected, units_to_move)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameList(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (permissions.IsAuthenticated,)


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GameSerializer
    lookup_field = 'id'


class MapDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Map.objects.all()
    serializer_class = MapSerializer
    lookup_field = 'id'

@api_view(['GET', 'POST',])
def update_tiles(request):
    if request.method == 'POST':
        serializer = TileSerializer(data=request.data, many=True)
        pprint(serializer)
        if serializer.is_valid():
            pprint(serializer.data)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print "NOT VALID", serializer.errors
        return Response(request.data, status=status.HTTP_201_CREATED)

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