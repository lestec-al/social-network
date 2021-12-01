from django import forms
from django.forms.widgets import PasswordInput
from .models import Notes, Images
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'text']

class UserForm(UserCreationForm):
    username = forms.CharField(min_length=8, max_length=150, help_text="")
    email = forms.EmailField(max_length=254, help_text="", required=True)
    password1 = forms.CharField(label="Password", help_text="", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", help_text="", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2' ]

class UserUpdateForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='', required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    password1 = forms.CharField(label="Password", help_text="", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", help_text="", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2' ]

class ImagesForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image']