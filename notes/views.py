from django.db.models import query
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Notes
from .forms import NotesForm

def index_view(request):
    return render(request,'index.html')

class NotesListView(View):
    template_name = 'notes/list.html'
    def get(self, request):
        queryset = Notes.objects.all()
        context = {'object_list': queryset}
        return render(request, self.template_name, context)

class NotesDetailView(View):
    template_name = 'notes/detail.html'
    def get(self, request, id):
        obj = get_object_or_404(Notes, id=id)
        #obj = Product.objects.get(id=id)
        context = {'object': obj}
        return render(request, self.template_name, context)

    def post(self, request, id):
        obj = get_object_or_404(Notes, id=id)
        #obj = Product.objects.get(id=id)
        if request.method == "POST":
            obj.delete()
            return redirect("../")
        context = {'object': obj}
        return render(request, self.template_name, context)

class NotesCreateView(View):
    template_name = 'notes/create.html'
    def get(self, request):
        form = NotesForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = NotesForm(request.POST or None)
        if form.is_valid():
                form.save()
                return redirect("../")
        return render(request, self.template_name, {'form': form})

class NotesUpdateView(View):
    template_name = 'notes/create.html'

    def get_object(self):
        id = self.kwargs.get("id")
        obj = get_object_or_404(Notes, id=id)
        return obj

    def get(self, request, id=None):
        context = {}
        obj = self.get_object()
        form = NotesForm(instance=obj)
        context['form'] = form
        context['object'] = obj
        return render(request, self.template_name, context)

    def post(self, request, id=None):
        context = {}
        obj = self.get_object()
        form = NotesForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("../")
        context['form'] = form
        context['object'] = obj
        return render(request, self.template_name, context)