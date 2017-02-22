# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpRequest
from TestChat.context_processors import users_processor


class ContextProcessorsTests(TestCase):
	fixtures = ['data.json']

	def test_users_processor(self):
		"""Test users processor"""
		request = HttpRequest()
		data = users_processor(request)
		# test data from processor
		self.assertEqual(len(data['users']), 2)
