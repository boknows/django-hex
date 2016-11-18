from django.shortcuts import render
from django.contrib.auth.models import User

from map.models import Game, GameMembership, GameLog, Map, Tile


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
