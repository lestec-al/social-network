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
from notes.views import NotesListView, NotesDetailView, NotesCreateView, NotesUpdateView, index_view

urlpatterns = [
    path("notes/", NotesListView.as_view(), name="notes"),
    path("notes/<int:id>/", NotesDetailView.as_view(), name="note_detail"),
    path("create_note/", NotesCreateView.as_view(), name="note_create"),
    path("notes/<int:id>/update_note/", NotesUpdateView.as_view(), name="note_update"),

    path("", index_view, name="home"),
    path('admin/', admin.site.urls),
]
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', include('django.contrib.auth.urls'), name='login'),
    path('logout/', include('django.contrib.auth.urls'), name='logout'),
    path('password_change/', include('django.contrib.auth.urls'), name='password_change'),
    path('password_change/done/', include('django.contrib.auth.urls'), name='password_change_done'),
    path('password_reset/', include('django.contrib.auth.urls'), name='password_reset'),
    path('password_reset/done/', include('django.contrib.auth.urls'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', include('django.contrib.auth.urls'), name='password_reset_confirm'),
    path('reset/done/', include('django.contrib.auth.urls'), name='password_reset_complete'),
]