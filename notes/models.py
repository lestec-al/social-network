from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Notes(models.Model):
    title = models.CharField(max_length=30)
    text = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("note_detail", kwargs={"id": self.id})
