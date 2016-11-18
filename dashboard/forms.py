from django import forms


class CreateGameForm(forms.Form):
    email1 = forms.EmailField()
    email2 = forms.EmailField(required=False)
    email3 = forms.EmailField(required=False)
    email4 = forms.EmailField(required=False)
    email5 = forms.EmailField(required=False)
    email6 = forms.EmailField(required=False)
    email7 = forms.EmailField(required=False)

