from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadhandler import InMemoryUploadedFile
from PIL import Image
import io

class Note(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    private = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[0:50]

    class Meta:
        ordering = ['-updated_at']

class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    note = models.ForeignKey("Note", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} like {self.note}"

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='uploads/avatars/', default="uploads/avatars/user.png", blank=True, null=True)
    about = models.TextField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self):
        if self.avatar.height > 300 or self.avatar.width > 300:
            img = Image.open(io.BytesIO(self.avatar.read()))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.thumbnail((300,300), Image.ANTIALIAS)
            output = io.BytesIO()
            img.save(output, format='JPEG')
            output.seek(0)
            self.avatar = InMemoryUploadedFile (output,'ImageField', "%s.jpg" %self.avatar.name.split('.')[0], 'image/jpeg',"Content-Type: charset=utf-8", None)
        super(Profile, self).save()

class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE, blank=True, null=True)
    note = models.ForeignKey("Note", on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[0:50]

    class Meta:
        ordering = ['-created_at']

class Room(models.Model):
    profiles = models.ManyToManyField("Profile", blank=True, null=True)

    def __str__(self):
        return str(self.id)

class Message(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE, blank=True, null=True)
    room = models.ForeignKey("Room", on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[0:50]

    class Meta:
        ordering = ['-created_at']