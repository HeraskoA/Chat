# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class TestAuth(TestCase):

    fixtures = ['data.json']

    def setUp(self):
        self.client = Client()

    def test_anon(self):
        """anon user, return 302 status code"""
        self.client.logout()
        response = self.client.get(reverse('dialog', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_auth(self):
        """authentication user, return status code 200"""
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse('dialog', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
