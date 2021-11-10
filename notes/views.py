from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Notes
from .forms import NotesForm, UserForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login

class NotesListView(LoginRequiredMixin, View):
    template_name = 'notes/list.html'
    def get(self, request):
        context = {}
        queryset = Notes.objects.filter(user=request.user.id)#.order_by("created_at")
        context['object_list'] = queryset
        return render(request, self.template_name, context)

    def post(self, request, id=None):
        try:
            context = {}
            queryset = Notes.objects.filter(user=request.user.id)
            for obj in queryset:
                if request.POST.get("delete" + str(obj.id)):
                    obj.delete()
                    return redirect("/")

                if request.POST.get("edit" + str(obj.id)):
                    obj1 = Notes.objects.get(id=obj.id, user=request.user.id)
                    form = NotesForm(instance=obj1)
                    context['form'] = form
                    context['object1'] = obj1
                    context['object_list'] = queryset
                    return render(request, self.template_name, context)

                if request.POST.get('save' + str(obj.id)):
                    obj1 = Notes.objects.get(id=obj.id, user=request.user.id)
                    form = NotesForm(request.POST, instance=obj1)
                    if form.is_valid():
                        form.save()
                        return redirect("/")
                    context['form'] = form
                    context['object1'] = obj1
                    context['object_list'] = queryset
                    return render(request, self.template_name, context)

                if request.POST.get('page' + str(obj.id)):
                    return redirect("/" + str(obj.id))

                if request.POST.get('cancel'):
                    return redirect("/")
        except:
            return render(request, 'links/error.html')

class NotesCreateView(LoginRequiredMixin, View):
    template_name = 'notes/create.html'
    def get(self, request):
        form = NotesForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = NotesForm(request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("/")
        return render(request, self.template_name, {'form': form})

class NotesDetailView(LoginRequiredMixin, View):
    template_name = 'notes/detail.html'

    def get(self, request, id=None):
        try:
            context = {}
            obj = Notes.objects.get(id=id, user=request.user.id)
            form = NotesForm(instance=obj)
            context['form'] = form
            context['object'] = obj
            return render(request, self.template_name, context)
        except:
            return render(request, 'notes/error.html')

    def post(self, request, id=None):
        try:
            context = {}
            obj = Notes.objects.get(id=id, user=request.user.id)
            if request.POST.get('save'):
                form = NotesForm(request.POST, instance=obj)
                if form.is_valid():
                    form.save()
                    return redirect("/")
                context['form'] = form
                context['object'] = obj
                return render(request, self.template_name, context)
            elif request.POST.get('delete'):
                if request.method == "POST":
                    obj.delete()
                    return redirect("/")
                context = {'object': obj}
                return render(request, self.template_name, context)
        except:
            return render(request, 'notes/error.html')

class SettingsView(LoginRequiredMixin, View):
    template_name = 'notes/settings.html'

    def get(self, request):
        return render(request, self.template_name, {})

class RegistrationView(View):
    template_name = 'registration/registration.html'

    def get(self, request):
        context = {}
        form = UserForm()
        context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request):
            context = {}
            g = Group.objects.get(name='Common Users')
            if request.POST.get('registration'):
                form = UserForm(request.POST)
                if form.is_valid():
                    form.save()
                    username = form.cleaned_data.get('username')
                    raw_password = form.cleaned_data.get('password1')
                    user = authenticate(username=username, password=raw_password)
                    login(request, user)
                    g.user_set.add(user.id)

                    return redirect("/")
                return render(request, self.template_name, {'form': form})