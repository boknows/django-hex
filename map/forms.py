from django import forms

from .models import Game, GameLog, Map


class NewGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('start_date')



