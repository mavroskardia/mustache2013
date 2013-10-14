# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render

def home(req):
    return render(req, 'voting/home.html', {'players':[1,2,3]})

def test(req):
    return render(req, 'voting/test.html', {})