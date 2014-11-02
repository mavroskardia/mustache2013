from django.db import models
from django.contrib.auth.models import User
from . import utils

class Gentleman(models.Model):
    # Make Gentleman a profile model based on Django's User model
    user = models.OneToOneField(User)

    name = models.CharField(max_length=256)
    tagline = models.CharField(max_length=1024,blank=True)
    before_pic = models.ImageField(upload_to='images',blank=True)
    before_pic_resized = models.ImageField(upload_to='images',blank=True)
    after_pic = models.ImageField(upload_to='images',blank=True)
    after_pic_resized = models.ImageField(upload_to='images',blank=True)

    def save(self, *args, **kwargs):
        #self.resize_if_needed()
        super(Gentleman, self).save(*args, **kwargs)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.name

    def resize_if_needed(self):
        if self.before_pic:
            thumb = utils.create_thumbnail(self.before_pic.file)
            fn = utils.create_thumbnail_name(self.before_pic.name)
            self.before_pic_resized.save(fn, thumb)

        if self.after_pic:
            thumb = utils.create_thumbnail(self.after_pic.file)
            fn = utils.create_thumbnail_name(self.after_pic.name)
            self.after_pic_resized.save(fn, thumb)


class Vote(models.Model):
    user = models.OneToOneField(User)
    execution = models.ForeignKey(Gentleman, null=True, blank=True, related_name='execution_set')
    grooming = models.ForeignKey(Gentleman, null=True, blank=True, related_name='grooming_set')
    creativity = models.ForeignKey(Gentleman, null=True, blank=True, related_name='creativity_set')

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return '%s\'s vote' % self.user.username

class Comment(models.Model):
    poster = models.ForeignKey(User)
    gentleman = models.ForeignKey(Gentleman)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        truncd = (self.text[:40] + '...') if len(self.text) > 40 else self.text
        return 'Comment about %s on %s: %s' % (self.gentleman.name, self.timestamp, truncd)