from django.shortcuts import render
from datetime import time
from django.contrib.auth.models import User
from TestChat.models import Dialog, Message, UserPhoto
from django.views.generic import UpdateView
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core import serializers
from django import forms
from TestChat.forms import UserForm, ProfileForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'chat/base.html', {})

@login_required
def ProfileView(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.userphoto)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'chat/profile.html', {
                'user_form': user_form,
                'profile_form': profile_form
            })
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userphoto)
    return render(request, 'chat/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def dialog(request, pk):
    user1 = request.user
    user2 = User.objects.get(id=int(pk))
    try:
        dialog = Dialog.objects.get(user1=user1, user2=user2)
    except Exception:
        dialog, created = Dialog.objects.get_or_create(user1=user2, user2=user1)
    if request.is_ajax():
        response_data = []
        if request.method == 'POST':
            text = request.POST.get('mess')
            Message.objects.create(text=text, sender=user1, dialog=dialog)
            return HttpResponse(json.dumps(0))
        else:
            count = int(request.GET.get('count'))
            messages = Message.objects.filter(dialog=dialog)
            if count != len(messages):
                messages = messages[count:]
                for message in messages:
                    response_data.append({
                        'text': message.text,
                        'sender': message.sender.username,
                        'time': time.strftime(message.date, "%H:%M")
                    })
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        messages = Message.objects.filter(dialog=dialog)
        count = len(messages)
        return render(request, 'chat/dialog.html', {'messages': messages, 'interlocutor': user2, 'count': count})
