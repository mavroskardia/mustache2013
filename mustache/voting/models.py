from django.db import models
from django.contrib.auth.models import User

class Gentleman(models.Model):
	# Make Gentleman a profile model based on Django's User model
	user = models.OneToOneField(User)
	
	name = models.CharField(max_length=256)
	tagline = models.CharField(max_length=1024)
	before_pic = models.ImageField(upload_to='images')
	after_pic = models.ImageField(upload_to='images')
	
	votes = models.ForeignKey('Vote')

class Vote(models.Model):
	execution = models.IntegerField()
	grooming = models.IntegerField()
	creativity = models.IntegerField()
