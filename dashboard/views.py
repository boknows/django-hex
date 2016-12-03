from __future__ import division

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from map.models import Game, GameMembership
from forms import CreateGameForm
from start_game import start_game




@login_required
def home(request):
    active_games = GameMembership.objects.filter(user=request.user)
    return render(request, "home.html", {
        'user': request.user,
        'active_games': active_games
    })


@login_required
def create_game(request):
    form = CreateGameForm()
    return render(request, "create_game.html", {
        'user': request.user,
        'form': form
    })


def start_game_submit(request):
    form = CreateGameForm()
    if request.method == 'POST':
        form = CreateGameForm(request.POST)
        if form.is_valid():
            start_game(request.user, form)

    return redirect('dashboard:home')




