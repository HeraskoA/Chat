# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from TestChat.models import Dialog, Message, UserPhoto
from django.db.models import CharField, ForeignKey, OneToOneField, ImageField
from io import BytesIO
from PIL import Image


class TestMessage(TestCase):

    fixtures = ['data.json']

    def test_model(self):
	user1 = User.objects.first()
	user2 = User.objects.last()
	dialog = Dialog.objects.create(user1=user1, user2=user2)
        Message.objects.create(
            text="text",
            sender=user1,
            dialog=dialog
        )
	message = Message.objects.first()
        text = message._meta.get_field('text')
        sender = message._meta.get_field('sender')
        dialog = message._meta.get_field('dialog')
        self.assertEqual(type(text), CharField)
        self.assertEqual(type(sender), ForeignKey)
        self.assertEqual(type(dialog), ForeignKey)

class TestDialog(TestCase):

    fixtures = ['data.json']

    def test_model(self):
	user1 = User.objects.first()
	user2 = User.objects.last()
	dialog = Dialog.objects.create(user1=user1, user2=user2)
	dialog = Dialog.objects.first()
        user1 = dialog._meta.get_field('user1')
        user2 = dialog._meta.get_field('user2')
        self.assertEqual(type(user1), ForeignKey)
        self.assertEqual(type(user2), ForeignKey)


class TestUserPhoto(TestCase):

    fixtures = ['data.json']

    def get_photo(self, width=200, height=200):
        """function that creates photo for next test"""
        photo = BytesIO()
        Image.new('RGBA',
                  (width, height),
                  color=(1, 1, 1)).save(photo, 'JPEG')
        photo.name = 'photo.jpeg'
        photo.seek(0)
        return photo

    def test_model(self):
	userphoto = UserPhoto.objects.first()
	userphoto.photo = self.get_photo()
	userphoto.save()
        user = userphoto._meta.get_field('user')
        photo = userphoto._meta.get_field('photo')
        self.assertEqual(type(user), OneToOneField)
        self.assertEqual(type(photo), ImageField)

    def test_photo_resize(self):
        """ test photo resizing """
	userphoto = UserPhoto.objects.first()
	userphoto.photo = self.get_photo(600, 600)
	userphoto.save()
        self.assertEqual(userphoto.photo.width, 300)
        self.assertEqual(userphoto.photo.height, 300)
