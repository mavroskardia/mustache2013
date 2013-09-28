# Create your views here.

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
import django.contrib.auth as auth

from models import Gentleman
from forms import LoginForm


def home(req):
    return render(req, 'voting/home.html', {'gentlemen': Gentleman.objects.all })

def test(req):
    return render(req, 'voting/test.html', {})

def signup(req):
	return render(req, 'voting/signup.html', {})

def login(req):

	if req.method == 'POST':
		login_form = LoginForm(req.POST)

		if login_form.is_valid():
			user = auth.authenticate(username=req.POST['username'], password=req.POST['password'])
			if user is not None:
				if user.is_active:
					auth.login(req, user)
					return home(req)
				else:
					messages.error(req, 'Not an active user')
			else:
				messages.error(req, 'Invalid username or password')
	else:
		login_form = LoginForm()

	return render(req, 'voting/login.html', {
		'login_form': login_form
	})

def profile(req):
	return render(req, 'voting/profile.html')

def logout(req):
	auth.logout(req)
	return home(req)