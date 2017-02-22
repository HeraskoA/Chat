from django.contrib.auth.models import User
from TestChat.models import UserPhoto
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserPhoto
        fields = ('photo',)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'




