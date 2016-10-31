from django.contrib import admin
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.models import User
from .models import  Dialog, Message, NumberMessages



admin.site.register(Dialog)
admin.site.register(Message)
admin.site.register(NumberMessages)
