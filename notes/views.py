from django.db.models import query
from django.http import request
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Notes
from .forms import NotesForm
from django.contrib.auth.models import User

class NotesListView(LoginRequiredMixin, View):
    template_name = 'notes/list.html'
    def get(self, request):
        queryset = Notes.objects.filter(user=request.user.id)
        context = {'object_list': queryset}
        return render(request, self.template_name, context)

class NotesDetailView(LoginRequiredMixin, View):
    template_name = 'notes/detail.html'
    def get(self, request, id):
        try:
            obj = get_object_or_404(Notes, id=id, user=request.user.id)
            context = {'object': obj}
            return render(request, self.template_name, context)
        except:
            return redirect("/")

    def post(self, request, id):
        obj = get_object_or_404(Notes, id=id)
        if request.method == "POST":
            obj.delete()
            return redirect("/")
        context = {'object': obj}
        return render(request, self.template_name, context)

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

class NotesUpdateView(LoginRequiredMixin, View):
    template_name = 'notes/create.html'

    def get(self, request, id=None):
        try:
            context = {}
            obj = get_object_or_404(Notes, id=id, user=request.user.id)
            form = NotesForm(instance=obj)
            context['form'] = form
            context['object'] = obj
            return render(request, self.template_name, context)
        except:
            return redirect("/")

    def post(self, request, id=None):
        try:
            context = {}
            obj = get_object_or_404(Notes, id=id, user=request.user.id)
            form = NotesForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                return redirect("/")
            context['form'] = form
            context['object'] = obj
            return render(request, self.template_name, context)
        except:
            return redirect("/")