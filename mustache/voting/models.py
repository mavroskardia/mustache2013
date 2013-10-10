from django.db import models
from django.contrib.auth.models import User

class Gentleman(models.Model):
	# Make Gentleman a profile model based on Django's User model
	user = models.OneToOneField(User)
	
	name = models.CharField(max_length=256)
	tagline = models.CharField(max_length=1024,blank=True)
	before_pic = models.ImageField(upload_to='images')
	before_pic_resized = models.ImageField(upload_to='images',blank=True)	
	after_pic = models.ImageField(upload_to='images',blank=True)
	after_pic_resized = models.ImageField(upload_to='images',blank=True)

	def save(self, *args, **kwargs):
#		self.resize_if_needed()
		super(Gentleman, self).save(*args, **kwargs)

	def __str__(self):
		return self.__unicode__()

	def __unicode__(self):
		return self.name

	def resize_if_needed(self):
		if not self.before_pic_resized:
			self.before_pic_resized = utils.create_thumbnail(self.before_pic)

		if self.after_pic and not self.after_pic_resized:
			self.after_pic_resized = utils.create_thumbnail(self.after_pic)

class Vote(models.Model):
	gentleman = models.OneToOneField(Gentleman)
	execution = models.IntegerField(default=0)
	grooming = models.IntegerField(default=0)
	creativity = models.IntegerField(default=0)

	def __str__(self):
		return self.__unicode__()

	def __unicode__(self):
		return '%s: Execution: %s Grooming: %s Creativity: %s' % (self.gentleman.name, self.execution, self.grooming, self.creativity)
