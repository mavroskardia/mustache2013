# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render

from models import Gentleman


def home(req):
    return render(req, 'voting/home.html', {'gentlemen': Gentleman.objects.all })

def test(req):
    return render(req, 'voting/test.html', {})