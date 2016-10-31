from django.shortcuts import render
from django.contrib.auth.models import User
from TestChat.models import Dialog, Message, NumberMessages
import json
from django.http import HttpResponse
from django.core import serializers
from django.views.generic.base import TemplateView


# Create your views here.
def home(request):
    return render(request, 'chat/base.html', {})


def dialog(request, pk):
    user = request.user
    user_id = int(pk)
    try:
        dialog = Dialog.objects.get(user1=user, user2=User.objects.get(id=user_id))
    except Exception:
        try:
            dialog = Dialog.objects.get(user1=User.objects.get(id=user_id), user2=user)
        except Exception:
            dialog = Dialog(user1=user, user2=User.objects.get(id=user_id))
            dialog.save()
    if request.is_ajax():
        response_data = []
        if request.method == 'POST':
            text = request.POST.get('mess')
            if text != '':
                message = Message(text=text, sender=user, dialog=dialog)
                message.save()
	messages = Message.objects.filter(dialog=dialog)
	num_mess = NumberMessages.objects.get(user = user, dialog = dialog)
	number = num_mess.number
	if number != len(messages):
		num_mess.number = len(messages)
		num_mess.save()
		messages = messages[(len(messages) - number):]
		for message in messages:
           		response_data.append({'text': message.text, 'sender': message.sender.username})	  
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        interlocutor = User.objects.get(id=user_id)
        messages = Message.objects.filter(dialog=dialog)
	number_of_messages, created = NumberMessages.objects.get_or_create(user = user, dialog = dialog)
	number_of_messages.number = len(messages)
	number_of_messages.save()
        return render(request, 'chat/dialog.html', {'messages': messages, 'interlocutor': interlocutor})



