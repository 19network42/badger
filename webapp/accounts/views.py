from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib import auth

from django.conf import settings
from .backends import oauth


def login(request):
    return render(request, "accounts/login.html")


def authenticate(request):
    api42 = oauth.create_client('api42')
    return api42.authorize_redirect(request, settings.API42_REDIRECT_URI)


def authorize(request):
    token = oauth.api42.authorize_access_token(request)
    user = auth.authenticate(request=request, token=token)
    if user is None:
        messages.error(request, 'Sorry, we could not authenticate you.')
        return redirect('/')
    else:
        auth.login(request, user)
        return redirect('/')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')
