from map.models import MAX_PLAYERS_TO_INVITE
from django.contrib.auth.models import User
from map.models import Game, Action, GameMembership, Map, Tile

import math
import random

def start_game(initiating_user, form):
    if form.is_valid():
        emails_that_exist = [initiating_user.email]
        emails_that_do_not_exist = []
        for i in range(1, MAX_PLAYERS_TO_INVITE):
            email = form.cleaned_data['email' + str(i)]
            if email:
                if User.objects.filter(email=email):
                    emails_that_exist.append(email)
                else:
                    emails_that_do_not_exist.append(email)

        # initial data
        users = User.objects.filter(email__in=emails_that_exist)
        game = Game.objects.create()
        for user in users:
            if user == initiating_user:
                membership_type = GameMembership.ACCEPTED
            else:
                membership_type = GameMembership.INVITED
            GameMembership.objects.create(user=user, game=game, membership_type=membership_type)
        for email in emails_that_do_not_exist:
            GameMembership.objects.create(email=email, game=game)

        radius = 25  # TODO: Global variable?
        game_map = Map.objects.create(
            game=game,
            rows=10,
            columns=10,
            radius=radius,
            side=round(3 / 2 * radius, 10),
            height=round(math.sqrt(3) * radius, 10),
            width=round(2 * radius, 10)
        )
        game_log = Action.objects.create(map=game_map)


def create_tiles(game):
        users = GameMembership.objects.filter(game=game, membership_type=GameMembership.ACCEPTED)
        game_map = Map.objects.get(game=game)
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
        while (tiles_list):
            assigned_tile = tiles_list[0]
            assigned_tile.owner = users[player_counter]
            assigned_tile.save()
            tiles_list.pop(0)
            if player_counter == player_total:
                player_counter = 0
            else:
                player_counter += 1

        game.status = Game.PLAYING
        game.save()

        return game
