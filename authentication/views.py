from django.shortcuts import render, redirect
from forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as log_user_in
from django.contrib.auth.models import User
from map.models import GameMembership


def login(request):
    form = LoginForm()
    user = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                log_user_in(request, user)
                return redirect('dashboard:home')

    return render(request, "login.html", {
        'form': form,
        'user': user
    })


def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            log_user_in(request, user)
            # Check for any GameMemberships they might have and convert to User references
            memberships = GameMembership.objects.filter(email=user.email)
            if memberships:
                for membership in memberships:
                    membership.user = user
                    membership.email = None
                    membership.save()
            return redirect('dashboard:home')

    return render(request, "register.html", {
        'form': form,
    })
