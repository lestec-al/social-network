from django.urls import path
from notes.views import *

urlpatterns = [
    path("", main_page_view, name="main"),
    path("back/", return_back_view, name="back"),
    path("<int:id>/", profile_view, name="profile"),
    path("notes/<int:id>/", note_view, name="note"),
    path('notes/<int:id>/delete/', delete_note_view, name="delete_note"),
    path('notes/comments/<int:id>/delete/', delete_comment_view, name="delete_comment"),
    path("settings/", settings_view, name="settings"),
    path("messages/", rooms_messages_view, name="messages_rooms"),
    path("messages/<int:id>/", room_messages_view, name="messages_room"),
    path('messages/message/<int:id>/delete/', delete_message_view, name="delete_message"),
    path("registration/", registration_view, name="registration"),
]