from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Images, Notes
from .forms import NotesForm, UserForm, UserUpdateForm, ImagesForm
from django.contrib.auth import login
from django.contrib.auth.models import User

class NotesListView(LoginRequiredMixin, View):
    template_name = 'notes/list.html'
    def get(self, request):
        search_str = request.GET.get("search", False)
        if search_str:
            queryset = Notes.objects.filter(user=request.user.id, title__contains=search_str).order_by("-updated_at") or Notes.objects.filter(user=request.user.id, text__contains=search_str).order_by("-updated_at")
        else:
            queryset = Notes.objects.filter(user=request.user.id).order_by("-updated_at")
        context = {}
        context['object_list'] = queryset
        try:
            avatar = Images.objects.get(user=request.user.id)
            context['avatar'] = avatar
        except: None
        return render(request, self.template_name, context)

    def post(self, request, id=None):
        context = {}
        queryset = Notes.objects.filter(user=request.user.id)
        context['object_list'] = queryset
        # Create notes on main page
        #notes = Notes.objects.create(user=request.user, title=request.POST.get("title"), text=request.POST.get("text"))
        #return redirect("/")
        if request.POST.get("new"):
            form = NotesForm()
            context['form'] = form
            return render(request, self.template_name, context)
        if request.POST.get("save"):
            form = NotesForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.save()
                return redirect("/")
            context['form'] = form
            return render(request, self.template_name, context)
        # Navigation
        if request.POST.get('cancel'):
            return redirect("/")
        for obj in queryset:
            if request.POST.get("delete" + str(obj.id)):
                obj.delete()
                return redirect("/")
            # Edit notes on main page
            if request.POST.get("edit" + str(obj.id)):
                obj1 = Notes.objects.get(id=obj.id, user=request.user.id)
                form = NotesForm(instance=obj1)
                context['form'] = form
                context['object1'] = obj1
                return render(request, self.template_name, context)
            if request.POST.get('save' + str(obj.id)):
                obj1 = Notes.objects.get(id=obj.id, user=request.user.id)
                form = NotesForm(request.POST, instance=obj1)
                if form.is_valid():
                    form.save()
                    return redirect("/")
                context['form'] = form
                context['object1'] = obj1
        return render(request, self.template_name, context)

class SettingsView(LoginRequiredMixin, View):
    template_name = 'notes/settings.html'
    def get(self, request):
        context = {}
        user = User.objects.get(id=request.user.id)
        update_user_form = UserUpdateForm(instance=user)
        context['update_user_form'] = update_user_form
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        if request.POST.get('update_account'):
            user = User.objects.get(id=request.user.id)
            update_user_form = UserUpdateForm(request.POST, instance=user)
            if update_user_form.is_valid():
                user = update_user_form.save(commit=False)
                user.save()
                return redirect("/settings/")
            context['update_user_form'] = update_user_form
            return render(request, self.template_name, context)

class RegistrationView(View):
    template_name = 'registration/registration.html'
    def get(self, request):
        form = UserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.POST.get('registration'):
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                login(request, user)
                return redirect("/")
            return render(request, self.template_name, {'form': form})