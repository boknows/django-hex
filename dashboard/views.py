from __future__ import division

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from forms import CreateGameForm
from start_game import start_game




@login_required
def home(request):
    return render(request, "home.html", {
        'user': request.user
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
    print request.__dict__
    if request.method == 'POST':
        form = CreateGameForm(request.POST)
        if form.is_valid():
            start_game(form)

    return redirect('dashboard:home')





