# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from TestChat.models import UserPhoto
from io import BytesIO
from PIL import Image


class TestProfileView(TestCase):

    fixtures = ['data.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username="admin", password="admin")

    def get_photo(self, width=200, height=200):
        """function that creates photo for next test"""
        photo = BytesIO()
        Image.new('RGBA',
                  (width, height),
                  color=(1, 1, 1)).save(photo, 'JPEG')
        photo.name = 'photo.jpeg'
        photo.seek(0)
        return photo

    def test_displaing_data_without_photo(self):
        """check displaing admin data without photo"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Username:', response.content)
        self.assertIn('Email:', response.content)
        self.assertIn('Save', response.content)
        self.assertIn('Cancel', response.content)
        self.assertIn('admin', response.content)
        self.assertIn('admin@admin.com', response.content)
        self.assertIn('anon.jpg', response.content)

    def test_displaing_data_with_photo(self):
        """check displaing admin data with photo"""
        response = self.client.get(reverse('profile'))
	user = User.objects.first()
	photo = UserPhoto.objects.get(user=user)
	photo.photo = self.get_photo()
	photo.save()
        self.assertEqual(response.status_code, 200)
        self.assertIn('Username:', response.content)
        self.assertIn('Email:', response.content)
        self.assertIn('Save', response.content)
        self.assertIn('Cancel', response.content)
        self.assertIn('admin', response.content)
        self.assertIn('admin@admin.com', response.content)
        self.assertTrue(user.userphoto.photo)

    def test_context(self):
        """check context"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user_form'])
        self.assertTrue(response.context['profile_form'])

    def test_post_form(self):
        """test form ability to save edited data"""
        self.client.post(reverse('profile'), {
            'username': 'namename',
            'email': 'em@em.com',
            'photo': self.get_photo()
        }, follow=True)
	user = User.objects.first()
        self.assertEqual(user.username, 'namename')
        self.assertEqual(user.email, 'em@em.com')
        self.assertTrue(user.userphoto.photo)

    def test_dialog_view_template(self):
        """check the use of the correct template"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/profile.html')
