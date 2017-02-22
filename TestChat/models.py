# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class Message(models.Model):
	text = models.CharField(max_length=256, blank=False)
	sender = models.ForeignKey(User, null=True)
	dialog = models.ForeignKey('Dialog', null=True)
	date = models.TimeField(auto_now_add = True)

	def __unicode__(self):
		return u"%s: %s" % (self.sender, self.text)

class Dialog(models.Model):
	user1 = models.ForeignKey(User, related_name='+')
	user2 = models.ForeignKey(User, related_name='+')

	def __unicode__(self):
		return u"%s and %s" % (self.user1, self.user2)

class UserPhoto(models.Model):
	user = models.OneToOneField(User)
	photo = models.ImageField(blank=True, null=True, upload_to='img/')

	def save(self, *args, **kwargs):
        	if self.photo:
            		image = Image.open(StringIO.StringIO(self.photo.read()))
            		image.thumbnail((300, 300), Image.ANTIALIAS)
            		output = StringIO.StringIO()
            		image.save(output, format='JPEG', quality=75)
            		output.seek(0)
            		self.photo = InMemoryUploadedFile(
                		output,
                		'ImageField',
                		"%s.jpg" % self.photo.name.split('.')[0],
                		'image/jpeg',
                		output.len,
                		None
            		)
        	super(UserPhoto, self).save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserPhoto.objects.create(user=instance)


