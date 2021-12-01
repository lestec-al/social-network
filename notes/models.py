from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

class Notes(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=50, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("note_detail", kwargs={"id": self.id})

    def __str__(self):
        return self.title

class Images(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return str(self.id)