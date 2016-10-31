# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
	text = models.CharField(
	max_length=256,
	blank=False,
	verbose_name=u"Сообщение")
	sender = models.ForeignKey(User, null=True)
	dialog = models.ForeignKey('Dialog', null=True)
	date = models.DateField(
	auto_now_add = True)
	def __unicode__(self):
		return u"%s: %s" % (self.sender, self.text)
class Dialog(models.Model):
	user1 = models.ForeignKey(User, related_name='+')
	user2 = models.ForeignKey(User, related_name='+')
	def __unicode__(self):
		return u"%s and %s" % (self.user1, self.user2)
class NumberMessages(models.Model):
	number = models.IntegerField(max_length = 256, default = 0)
	user = models.ForeignKey(User)
	dialog = models.ForeignKey(Dialog)
	def __unicode__(self):
		return u"%s: %s" % (self.dialog, self.user)


