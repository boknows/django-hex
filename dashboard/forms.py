from django import forms
from django.contrib.auth.models import User


class CreateGameForm(forms.Form):
    username = forms.CharField(label='Username', max_length=32)
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data['email']
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise forms.ValidationError("This email is already associated with a user.")
        else:
            return self.cleaned_data
