from django.contrib import admin
from .models import Note, Profile, Comment, Like, Room, Message

admin.site.register(Note)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Room)
admin.site.register(Message)