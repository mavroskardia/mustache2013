# Create your views here.

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
import django.contrib.auth as auth
from django.contrib.auth.models import User

from models import Gentleman
from forms import LoginForm,SignupForm,ProfileForm


def home(req):
    return render(req, 'voting/home.html', {'gentlemen': Gentleman.objects.all })

def test(req):
    return render(req, 'voting/test.html', {})

def signup(req):
    if req.method == 'POST':
        signup_form = SignupForm(req.POST, req.FILES)
        if signup_form.is_valid():
            try:
                user = User.objects.create_user(signup_form.cleaned_data['username'], None, signup_form.cleaned_data['password'])
                gentleman = Gentleman()
                gentleman.user_id = user.id
                gentleman.name = signup_form.cleaned_data['username']
                gentleman.tagline = signup_form.cleaned_data['tagline']
                gentleman.before_pic.file = req.FILES['before_pic']
                gentleman.save()
            except Exception as e:
                messages.error(req, e)
            return HttpResponseRedirect(reverse('home'))
    else:
        signup_form = SignupForm()
    return render(req, 'voting/signup.html', {'signup_form': signup_form})

def login(req):

	if req.method == 'POST':
		login_form = LoginForm(req.POST)

		if login_form.is_valid():
			user = auth.authenticate(username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
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

	g = get_object_or_404(Gentleman, pk=req.user.gentleman.id)

	if req.method == 'POST':
		pf = ProfileForm(req.POST, req.FILES, instance=g)

		if pf.is_valid():
			ng = pf.save()

			if 'before_pic' in req.FILES:
				g.before_pic.file = req.FILES['before_pic']
			if 'after_pic' in req.FILES:
				g.after_pic.file = req.FILES['after_pic']

			ng.user_id = g.user_id
			ng.id = g.id
			ng.save()

			pf = ProfileForm(instance=ng)

			messages.info(req, 'Gentleman updated successfully.')

	else:
		pf = ProfileForm(instance=g)

	return render(req, 'voting/profile.html', {'pf': pf })

def logout(req):
	auth.logout(req)
	return home(req)