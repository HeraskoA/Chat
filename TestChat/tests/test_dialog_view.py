# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from TestChat.models import Dialog, Message, UserPhoto
from datetime import time
import json


class TestDialogView(TestCase):

    fixtures = ['data.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username="admin", password="admin")
        self.url = reverse('dialog', kwargs={'pk': 2})
	self.client.get(self.url)
        sender1 = User.objects.first()
        sender2 = User.objects.last()
        dialog = Dialog.objects.first()
        for i in range(10):
            Message.objects.create(text='text', sender=sender1, dialog=dialog)
        for i in range(10):
            Message.objects.create(text='text', sender=sender2, dialog=dialog)
	self.count = Message.objects.count()

    def test_displaing_data(self):
        """check displaing data"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        for message in Message.objects.all():
            self.assertIn(message.text.encode('ascii','ignore'), response.content)
            self.assertIn(message.sender.username.encode('ascii','ignore'), response.content)
        self.assertEqual(len(response.context['messages']), 20)

    def test_send_message(self):
	"""check ability to save message"""
        self.client.post(
            path=self.url,
            data={
                "mess": "ajax"
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        new_count = Message.objects.count()
        last_message = Message.objects.last().text
        self.assertEqual(new_count, self.count+1)
        self.assertEqual(last_message, 'ajax')

    def test_get_messages_ajax(self):
	"""test get last unread messgaes"""
        response = self.client.get(
            path=self.url,
            data={
                "count": 5
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        messages = Message.objects.all()[5:]
        required_response = []
        for message in messages:
            required_response.append({
                'text': message.text,
                'sender': message.sender.username,
                'time': time.strftime(message.date, "%H:%M")
            })
        required_response = json.dumps(required_response)
        self.assertEqual(response.content, required_response)

    def test_dialog_view_template(self):
        """check the use of the correct template"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/dialog.html')
