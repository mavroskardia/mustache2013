# Create your views here.
try:
    from itertools import zip_longest   # supporting >=3.4
except ImportError:
    from itertools import izip_longest as zip_longest  # supporting <3.4

from random import shuffle

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
import django.contrib.auth as auth
from django.contrib.auth.models import User

from .models import Gentleman,Vote,Comment
from .forms import LoginForm,ParticipateForm,ProfileForm,CommentForm


def home(req):    
    gents = list(Gentleman.objects.all())                   # get everybody (would eventually page this)
    shuffle(gents)                                          # shuffle the list so there is a different order each time
    it = iter(gents)                                        # convert the list into an iterable so we can use zip_longest
    paired_gents = zip_longest(*[it] * 2, fillvalue=None)   # pair up the members of the list, if the length is odd, fill in with None

    return render(req, 'voting/home.html', {'pairs_of_gents': paired_gents, 'gentlemen': gents, 'comment_form': CommentForm() })

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
                gentleman.name = participate_form.cleaned_data['name']
                gentleman.tagline = participate_form.cleaned_data['tagline']
                gentleman.before_pic = participate_form.cleaned_data['before_pic']
                gentleman.save()

                gentleman.resize_if_needed()

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
                    return HttpResponseRedirect(reverse('home'))
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

            resize = False

            if 'before_pic' in req.FILES:
                g.before_pic = req.FILES['before_pic']
                resize = True
            if 'after_pic' in req.FILES:
                g.after_pic = req.FILES['after_pic']
                resize = True

            ng.user_id = g.user_id
            ng.id = g.id
            ng.save()

            if resize:
                ng.resize_if_needed()

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

        try:
            vote = Vote.objects.get(user=req.user)
        except Vote.DoesNotExist:
            vote = Vote()
            vote.user_id = req.user.id

        if 'execution' in req.POST:
            vote.execution_id = req.POST['execution']

        if 'grooming' in req.POST:
            vote.grooming_id = req.POST['grooming']

        if 'creativity' in req.POST:
            vote.creativity_id = req.POST['creativity']

        vote.save()

        messages.info(req, 'Placed your vote!')

    return HttpResponseRedirect(reverse('home'))

def comment(req):
    if req.method == 'POST' and 'text' in req.POST and req.POST['text']:
        g = get_object_or_404(Gentleman, pk=req.POST['gentleman_id'])

        cf = CommentForm(req.POST)

        if cf.is_valid():
            c = Comment()
            c.poster = req.user
            c.gentleman = g
            c.text = cf.cleaned_data['text']
            c.save()

            messages.info(req, 'Added comment!')

    return HttpResponseRedirect(reverse('home'))

def logout(req):
    auth.logout(req)
    return HttpResponseRedirect(reverse('home'))

def results(req):

    voters = User.objects.all()
    votes = Vote.objects.all()
    turnout = len(votes) * 100.0 / len(voters)

    return render(req,
        'voting/results.html', {
            'gentlemen': Gentleman.objects.all(),
            'votes': votes,
            'voters': voters,
            'turnout': turnout
        })