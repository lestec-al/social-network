from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

class Notes(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=30)
    text = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("note_detail", kwargs={"id": self.id})
