from __future__ import division

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from map.models import Game, GameLog, GameMembership, Map

import math
import random



@login_required
def home(request):
    return render(request, "home.html", {
        'user': request.user
    })


@login_required
def create_game(request):
    return render(request, "create_game.html", {
        'user': request.user
    })


@login_required
@require_http_methods(["POST"])
def start_game(request):
    # initial data
    users = User.objects.all()
    game = Game.objects.create()
    for user in users:
        GameMembership.objects.create(user=user, game=game)

    radius = 25  # TODO: Global variable?
    game_map = Map.objects.create(
        game=game,
        rows=10,
        columns=10,
        radius=radius,
        side=round(3/2*radius,10),
        height=round(math.sqrt(3)*radius,10),
        width=round(2*radius,10)
    )
    game_log = GameLog.objects.create(game=game)

    # Create Tiles
    for row in range(game_map.rows):
        for column in range(game_map.columns):
            Tile.objects.create(map=game_map, row=row, column=column)

    # Shuffle tiles in a list, and assign players
    tiles_list = []
    tiles = Tile.objects.filter(map=game_map)
    for tile in tiles:
        tiles_list.append(tile)
    random.shuffle(tiles_list)

    player_counter = 0
    player_total = len(users) - 1
    while(tiles_list):
        assigned_tile = tiles_list[0]
        assigned_tile.owner = users[player_counter]
        assigned_tile.save()
        tiles_list.pop(0)
        if player_counter == player_total:
            player_counter = 0
        else:
            player_counter += 1

    return redirect('dashboard:home')





