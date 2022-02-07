from django import forms
from .models import Message, Note, Profile, Comment, Message
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class NotesForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text', 'private']

class UserForm(UserCreationForm):
    username = forms.CharField(min_length=8, max_length=150, help_text="")
    email = forms.EmailField(max_length=254, help_text="", required=True)
    password1 = forms.CharField(label="Password", help_text="", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", help_text="", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2' ]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =  ['about', 'avatar']

    def clean_avatar(self):
        if self.changed_data == ['avatar']:
            avatar = self.cleaned_data.get('avatar', False)
            if avatar:
                if avatar.size > 1100000:
                    raise ValidationError("Please upload a picture smaller than 1 MB")
                return avatar

class CommentForm(forms.ModelForm):
    text = forms.CharField(min_length=3)
    class Meta:
        model = Comment
        fields = ['text']

class MessageForm(forms.ModelForm):
    text = forms.CharField(min_length=3)
    class Meta:
        model = Message
        fields = ['text']