from map.models import MAX_PLAYERS_TO_INVITE
from django.contrib.auth.models import User
from map.models import Game, Action, GameMembership, Tile

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

        radius = 25  # TODO: Global variable?
        game = Game.objects.create(
            rows=10,
            columns=10,
            radius=radius,
            side=round(3 / 2 * radius, 10),
            height=round(math.sqrt(3) * radius, 10),
            width=round(2 * radius, 10)
        )
        # initial data
        users = User.objects.filter(email__in=emails_that_exist)
        for user in users:
            if user == initiating_user:
                membership_type = GameMembership.ACCEPTED
            else:
                membership_type = GameMembership.INVITED
            GameMembership.objects.create(user=user, game=game, membership_type=membership_type)
        for email in emails_that_do_not_exist:
            GameMembership.objects.create(email=email, game=game)

        game_log = Action.objects.create(game=game)


def create_tiles(game):
        memberships = GameMembership.objects.filter(game=game, membership_type=GameMembership.ACCEPTED)
        # Create Tiles
        for row in range(game.rows):
            for column in range(game.columns):
                Tile.objects.create(game=game, row=row, column=column)

        # Shuffle tiles in a list, and assign players
        tiles_list = []
        tiles = Tile.objects.filter(game=game)
        for tile in tiles:
            tiles_list.append(tile)
        random.shuffle(tiles_list)

        player_counter = 0
        player_total = len(memberships) - 1
        while (tiles_list):
            assigned_tile = tiles_list[0]
            assigned_tile.owner = memberships[player_counter].user
            assigned_tile.units = 3
            assigned_tile.save()
            tiles_list.pop(0)
            if player_counter == player_total:
                player_counter = 0
            else:
                player_counter += 1

        # Pick who's turn it is, randomly
        turn_player = random.randint(0, player_total)
        game.turn_player = memberships[turn_player].user

        game.status = Game.PLAYING
        game.save()

        return game
