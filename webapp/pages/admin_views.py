from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib import auth
from django.conf import settings
from accounts.backends import oauth
from accounts.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def login(request):
	return render(request, "login.html")


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
	messages.success(request, ("You were logged out!"))
	return redirect('/')


@login_required(login_url='pages:login')
@csrf_exempt
def user_page(request):
	context = {
		'users': User.objects.all(),
	}
	return render(request, "user.html", context)
