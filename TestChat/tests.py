# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from TestChat.models import Dialog, Message
from django.contrib.auth.models import User

class TestHomeView(TestCase):
	fixtures = ['home.json']
	def setUp(self):
		self.client = Client()
		self.url = reverse('home')
	def test_home_view(self):
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)
		self.assertIn('Чтобы воспользоваться', response.content)
		self.assertIn('admin1', response.content)
		self.assertIn('admin2', response.content)
		self.assertIn('Login', response.content)
		self.assertEqual(len(response.context['users']), 2)
	def test_home_view_is_auth(self):
		self.client.login(username='admin1', password='admin')
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)
		self.assertIn('Выберите собеседника', response.content)
		self.assertIn('Logout', response.content)
		self.assertIn('admin2', response.content)
		self.assertEqual(len(response.context['users']), 2)
class TestDialogView(TestCase):
	fixtures = ['dialog.json']
	def setUp(self):
		self.client = Client()
		self.url = reverse('dialog', kwargs={'pk': 2})
	def test_home_view_is_auth(self):
		self.client.login(username='admin1', password='admin')
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)
		self.assertIn('Пользователи', response.content)
		self.assertIn('Сообщение', response.content)
		self.assertIn('qwertyu', response.content)
		self.assertIn('qwerty', response.content)
		self.assertIn('Submit', response.content)
		self.assertEqual(len(response.context['users']), 3)



