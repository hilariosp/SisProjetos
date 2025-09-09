# barema/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Barema
from .forms import BaremaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

@login_required
def index(request):
    baremas = Barema.objects.all()
    return render(request, 'barema/index.html', {'baremas': baremas})

@login_required
def detail(request, id_barema):
    barema = get_object_or_404(Barema, id=id_barema)
    return render(request, 'barema/detail.html', {'barema': barema})

@login_required
@permission_required('barema.add_barema', raise_exception=True)
def add(request):
    if request.method == 'POST':
        form = BaremaForm(request.POST)
        if form.is_valid():
            # ModelForms com ManyToMany precisam primeiro salvar a instância principal
            barema_instance = form.save(commit=False)
            barema_instance.save()
            # E depois salvar a relação ManyToMany
            form.save_m2m()
            return HttpResponseRedirect('/barema/')
    else:
        form = BaremaForm()

    return render(request, 'barema/add.html', {'form': form})

@login_required
@permission_required('barema.change_barema', raise_exception=True)
def update(request, id_barema):
    barema = get_object_or_404(Barema, id=id_barema)

    if request.method == 'POST':
        form = BaremaForm(request.POST, instance=barema)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/barema/')
    else:
        form = BaremaForm(instance=barema)

    return render(request, 'barema/update.html', {'form': form})

@login_required
@permission_required('barema.delete_barema', raise_exception=True)
def delete(request, id_barema):
    Barema.objects.filter(id=id_barema).delete()
    return HttpResponseRedirect('/barema/')