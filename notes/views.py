from email.mime import message
from unicodedata import name
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Like, Note, Profile, Comment, Message, Room
from .forms import NotesForm, UserForm, UserProfileForm, CommentForm, MessageForm

@login_required
def return_back_view(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def rooms_messages_view(request):
    context = {}
    # Logged user
    request_user_profile = Profile.objects.get(user=request.user)
    context['request_user'] = request.user
    context['request_user_profile'] = request_user_profile
    # Rooms + delete room
    rooms = Room.objects.filter(profiles__user=request.user)
    for room in rooms:
        if request.POST.get('delete_room' + str(room.id)):
            obj = Room.objects.get(id=room.id)
            obj.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context['rooms'] = rooms
    return render(request, 'notes/messages.html', context)

@login_required
def room_messages_view(request, id):
    context = {}
    # Logged user
    request_user_profile = Profile.objects.get(user=request.user)
    context['request_user'] = request.user
    context['request_user_profile'] = request_user_profile
    # Rooms + delete room
    rooms = Room.objects.filter(profiles__user=request.user)
    for room in rooms:
        if request.POST.get('delete_room' + str(room.id)):
            obj = Room.objects.get(id=room.id)
            obj.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context['rooms'] = rooms
    # Room
    room = Room.objects.get(id=id, profiles__user=request.user)
    messages = Message.objects.filter(room=room)
    context['messages'] = messages
    context['room_selected'] = room
    # Create messages
    message_form = MessageForm()
    if request.POST.get('send_message'):
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message_form = message_form.save(commit=False)
            message_form.user = request.user
            message_form.profile = request_user_profile
            message_form.room = room
            message_form.save()
            return redirect(reverse("messages_room", kwargs={"id": id}))
    context['message_form'] = message_form
    for message in messages:
        # Edit massages
        if request.POST.get('edit_message' + str(message.id)):
            message1 = Message.objects.get(id=message.id, user=request.user)
            message_form = MessageForm(instance=message1)
            context['message_form_edit'] = message_form
            context['message1'] = message1
        if request.POST.get('save_edit_message' + str(message.id)):
            message1 = Message.objects.get(id=message.id, user=request.user)
            message_form = MessageForm(request.POST, instance=message1)
            if message_form.is_valid():
                message_form.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            context['message_form_edit'] = message_form
            context['message1'] = message1
    return render(request, 'notes/messages.html', context)

@login_required
def profile_view(request, id):
    context = {}
    # Load profile notes
    if id == request.user.id:
        queryset = Note.objects.filter(user=id)
    else:
        queryset = Note.objects.filter(user=id, private=False)
    context['object_list'] = queryset
    # Profile
    user_main = User.objects.get(id=id)
    profile_main = Profile.objects.get(user=user_main)
    context['user_main'] = user_main
    context['profile_main'] = profile_main
    # Logged user
    request_user_profile = Profile.objects.get(user=request.user)
    context['request_user'] = request.user
    context['request_user_profile'] = request_user_profile
    # Create notes
    if request.POST.get('new'):
        new_form = NotesForm()
        context['form'] = new_form
    if request.POST.get('save'):
        new_form = NotesForm(request.POST)
        if new_form.is_valid():
            nf = new_form.save(commit=False)
            nf.user = request.user
            nf.profile = request_user_profile
            nf.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        context['form'] = new_form
    # Send message to user, create room or redirect
    if request.POST.get('send_message_to'):
        uniq_room_id = int(f"{request_user_profile.user.id}{profile_main.user.id}")
        try:
            room = Room.objects.create(id=uniq_room_id)
            room.profiles.add(request_user_profile, profile_main)
        except:None
        return redirect(reverse("messages_room", kwargs={"id": uniq_room_id}))
    return render(request, 'notes/profile.html', context)

@login_required
def main_page_view(request):
    context = {}
    # Load notes + search users, notes
    search_str = request.GET.get("search", False)
    if search_str:
        queryset1 = Note.objects.filter(user=request.user.id, text__contains=search_str)
        queryset2 = Note.objects.filter(private=False, text__contains=search_str)
        queryset = queryset1 | queryset2
        try:
            queryset_people = User.objects.filter(username__contains=search_str)
            context['people_list'] = queryset_people
        except:None
    else:
        queryset = Note.objects.filter(private=False)
    context['object_list'] = queryset
    # Logged user
    context['request_user'] = request.user
    context['request_user_profile'] = Profile.objects.get(user=request.user)
    return render(request, 'notes/home.html', context)

@login_required
def note_view(request, id):
    context = {}
    obj = Note.objects.get(id=id)
    context['object'] = obj
    # Logged user
    request_user_profile = Profile.objects.get(user=request.user)
    context['request_user'] = request.user
    context['request_user_profile'] = request_user_profile
    # Likes
    if request.POST.get('like' + str(obj.id)):
        try:
            uniq_like_id = int(f"{request.user.id}{obj.id}")
            Like.objects.create(user=request.user, note=obj, id=uniq_like_id)
        except:None
    # Edit notes
    if request.POST.get('edit' + str(obj.id)):
        obj_edit = Note.objects.get(id=obj.id, user=request.user.id)
        edit_form = NotesForm(instance=obj_edit)
        context['form'] = edit_form
        context['object1'] = obj_edit
    if request.POST.get('save' + str(obj.id)):
        obj_edit = Note.objects.get(id=obj.id, user=request.user.id)
        edit_form = NotesForm(request.POST, instance=obj_edit)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        context['form'] = edit_form
        context['object1'] = obj_edit 
    # Comments
    comment_form = CommentForm()
    context['comment_form'] = comment_form
    context['comment_obj'] = obj
    if request.POST.get('save_comment' + str(obj.id)):
        comment_obj = Note.objects.get(id=obj.id)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form = comment_form.save(commit=False)
            comment_form.user = request.user
            comment_form.profile = request_user_profile
            comment_form.note = obj
            comment_form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        context['comment_form'] = comment_form
        context['comment_obj'] = comment_obj
    comments = Comment.objects.filter(note=obj)
    for comment in comments:
        # Edit comments
        if request.POST.get('edit_comment' + str(comment.id)):
            comment1 = Comment.objects.get(id=comment.id, user=request.user)
            comment_form = CommentForm(instance=comment1)
            context['comment_form_edit'] = comment_form
            context['comment1'] = comment1
        if request.POST.get('save_edit_comment' + str(comment.id)):
            comment1 = Comment.objects.get(id=comment.id, user=request.user)
            comment_form = CommentForm(request.POST, instance=comment1)
            if comment_form.is_valid():
                comment_form.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            context['comment_form_edit'] = comment_form
            context['comment1'] = comment1
    return render(request, 'notes/detail.html', context)

@login_required
def delete_note_view(request, id):
    obj = get_object_or_404(Note, id=id, user=request.user)
    obj.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def delete_comment_view(request, id):
    obj = get_object_or_404(Comment, id=id)
    if obj.user == request.user or obj.note.user == request.user:
        obj.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def delete_message_view(request, id):
    obj = get_object_or_404(Message, id=id)
    if obj.user == request.user:
        obj.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def settings_view(request):
    context = {}
    profile = Profile.objects.get(user=request.user)
    update_user_form = UserForm(request.POST or None, instance=request.user)
    #update_user_form = PasswordChangeForm(user=request.user, data=request.POST or None)
    update_profile_user_form = UserProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if request.POST.get('update_account'):
        if update_user_form.is_valid() and update_profile_user_form.is_valid():
            if update_profile_user_form.changed_data == ['avatar']:
                if Profile.objects.get(user=request.user).avatar:
                    Profile.objects.get(user=request.user).avatar.delete()
            update_profile_user_form.save()
            update_user_form.save()
            # Login after change set
            user = authenticate(request, username=update_user_form.cleaned_data["username"], password=update_user_form.cleaned_data["password1"])
            login(request, user)
            return redirect("/settings/")
    context['update_user_form'] = update_user_form
    context['update_profile_user_form'] = update_profile_user_form
    context['request_user'] = request.user
    context['request_user_profile'] = profile
    return render(request, 'notes/settings.html', context)

def registration_view(request):
    form = UserForm(request.POST or None)
    if request.POST.get('registration'):
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect("/")
    return render(request, 'registration/registration.html', {'form': form})