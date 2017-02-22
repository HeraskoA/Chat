# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from TestChat.models import Dialog, Message, UserPhoto


class TestHomeView(TestCase):

    fixtures = ['data.json']

    def setUp(self):
        self.client = Client()
        self.url = reverse('home')
        self.client.login(username="admin", password="admin")

    def test_displaing_data(self):
        """database coitains 1 object, must be present data in the page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Chat', response.content)
        self.assertIn('select the person', response.content)
        self.assertIn('Users', response.content)
        user1 = User.objects.first()
        user2 = User.objects.last()
        self.assertIn(user1.username, response.content)
        self.assertIn(user2.username, response.content)
        self.assertIn('Logout', response.content)

    def test_home_view_template(self):
        """check the use of the correct template"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/base.html')
