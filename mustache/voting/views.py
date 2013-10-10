# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render

def home(req):
    return render(req, 'voting/home.html', {})

def test(req):
    return render(req, 'voting/test.html', {})