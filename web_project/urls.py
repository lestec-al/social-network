"""web_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from notes.views import (
    profile_view, main_page_view, registration_view, settings_view,
    rooms_messages_view, room_messages_view, return_back_view,
    delete_note_view, delete_comment_view, note_view,
    delete_message_view
    )

urlpatterns = [
    path("", main_page_view, name="main"),
    path("back/", return_back_view, name="back"),
    path("<int:id>/", profile_view, name="profile"),
    path("note/<int:id>/", note_view, name="note"),
    path('note/<int:id>/delete/', delete_note_view, name="delete_note"),
    path('note/comments/<int:id>/delete/', delete_comment_view, name="delete_comment"),
    path('admin/', admin.site.urls),
    path("settings/", settings_view, name="settings"),
    path("messages/", rooms_messages_view, name="messages_rooms"),
    path("messages/<int:id>/", room_messages_view, name="messages_room"),
    path('messages/message/<int:id>/delete/', delete_message_view, name="delete_message"),
    path("registration/", registration_view, name="registration"),
    path('accounts/', include('django.contrib.auth.urls'))
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)