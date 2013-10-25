# Create your views here.

from random import shuffle

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
import django.contrib.auth as auth
from django.contrib.auth.models import User

from models import Gentleman,Vote
from forms import LoginForm,ParticipateForm,ProfileForm


def home(req):
    gents = list(Gentleman.objects.all())
    shuffle(gents)

    return render(req, 'voting/home.html', {'gentlemen': gents })

def test(req):
    return render(req, 'voting/test.html', {})

def register(req):
    if req.method == 'POST':
        register_form = LoginForm(req.POST)
        if register_form.is_valid():
            try:
                user = User.objects.create_user(register_form.cleaned_data['username'], None, register_form.cleaned_data['password'])
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth.login(req, user)
                return HttpResponseRedirect(reverse('home'))
            except Exception as e:
                messages.error(req, e)
    else:
        register_form = LoginForm()

    return render(req, 'voting/register.html', { 'register_form':register_form } )

def participate(req):
    if req.method == 'POST':
        participate_form = ParticipateForm(req.POST, req.FILES)
        if participate_form.is_valid():
            try:
                user = User.objects.create_user(participate_form.cleaned_data['username'], None, participate_form.cleaned_data['password'])
                gentleman = Gentleman()
                gentleman.user_id = user.id
                gentleman.name = participate_form.cleaned_data['username']
                gentleman.tagline = participate_form.cleaned_data['tagline']
                gentleman.before_pic = participate_form.cleaned_data['before_pic']
                gentleman.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth.login(req, user)
            except Exception as e:
                messages.error(req, e)
            return HttpResponseRedirect(reverse('home'))
    else:
        participate_form = ParticipateForm()
    return render(req, 'voting/participate.html', {'participate_form': participate_form})

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

def vote(req):

    if req.method == 'POST':

        if not req.user.is_authenticated():
            messages.warning(req, 'You need to login before you can vote')
            return HttpResponseRedirect(reverse('voting:login'))

        vote_target = get_object_or_404(Gentleman, pk=req.POST['gentleman_id'])
        try:
            vote = Vote.objects.get(user=req.user)
        except Vote.DoesNotExist:
            vote = Vote()
            vote.user_id = req.user.id

        if 'execution' in req.POST:
            vote.execution = vote_target

        if 'grooming' in req.POST:
            vote.grooming = vote_target

        if 'creativity' in req.POST:
            vote.creativity = vote_target

        vote.save()

        messages.info(req, 'Placed your vote!')

    return HttpResponseRedirect(reverse('home'))

def logout(req):
    auth.logout(req)
    return home(req)