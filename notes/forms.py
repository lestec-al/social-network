from django import forms
from .models import Notes, Avatar
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'text']

class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2' ]

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['image']