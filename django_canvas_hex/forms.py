from django import forms


class NewGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('start_date')