from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Equipe
from .forms import EquipeForm
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def index(request): 

    equipes = Equipe.objects.all()
    return render(request, 'equipe/index.html', {'equipes': equipes})

@login_required
def detail(request, id_equipe):

    equipe = Equipe.objects.get(id=id_equipe)
    return render(request, 'equipe/detail.html', {'equipe': equipe})

@login_required
@permission_required('equipe.add_equipe', raise_exception=True)
def add(request): 

    if request.method == 'POST':

        form = EquipeForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/equipe/')
    else:
        form = EquipeForm()

    return render(request, 'equipe/add.html', { 'form': form })

@login_required
@permission_required('equipe.change_equipe', raise_exception=True)
def update(request, id_equipe):

    equipe = Equipe.objects.get(id=id_equipe)

    if request.method == 'POST':

        form = EquipeForm(request.POST, instance=equipe)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/equipe/')
    else:
        form = EquipeForm(instance=equipe)

    return render(request, 'equipe/update.html', { 'form': form })

@login_required
@permission_required('equipe.delete_equipe', raise_exception=True)
def delete(request, id_equipe):

    Equipe.objects.filter(id=id_equipe).delete()

    return HttpResponseRedirect('/equipe/')


