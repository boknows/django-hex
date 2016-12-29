from django import forms

from .models import Game, GameMembership, Action, Map


class NewGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['start_date']


class InvitedForm(forms.ModelForm):
    CHOICES = (
        ('accepted', 'Accept'),
        ('declined', 'Decline'),
    )
    membership_type = forms.ChoiceField(choices=CHOICES, required=True, label='Reponse to invite')

    class Meta:
        model = GameMembership
        fields = ['membership_type', 'id', 'game', 'user']
        widgets = {
            'id': forms.HiddenInput(),
            'game': forms.HiddenInput(),
            'user': forms.HiddenInput(),
        }




