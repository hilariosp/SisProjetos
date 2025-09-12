from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Avaliacao, Usuario  
from .forms import AvaliacaoForm
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('avaliacao.view_avaliacao', raise_exception=True)
def index(request): 

    avaliacoes = Avaliacao.objects.all()
    return render(request, 'avaliacao/index.html', {'avaliacoes': avaliacoes})

@login_required
def detail(request, id_avaliacao):

    avaliacao = Avaliacao.objects.get(id=id_avaliacao)
    return render(request, 'avaliacao/detail.html', {'avaliacao': avaliacao})

@login_required
@permission_required('avaliacao.add_avaliacao', raise_exception=True)
def add(request): 

    if request.method == 'POST':

        form = AvaliacaoForm(request.POST)

        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.avaliador = Usuario.objects.get(id=request.user.id)
            avaliacao.save()
            form.save_m2m()
            return HttpResponseRedirect('/avaliacao/')
    else:
        form = AvaliacaoForm()

    return render(request, 'avaliacao/add.html', { 'form': form })

@login_required
@permission_required('avaliacao.change_avaliacao', raise_exception=True)
def update(request, id_avaliacao):

    avaliacao = Avaliacao.objects.get(id=id_avaliacao)

    if request.method == 'POST':

        form = AvaliacaoForm(request.POST, instance=avaliacao)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/avaliacao/')
    else:
        form = AvaliacaoForm(instance=avaliacao)

    return render(request, 'avaliacao/update.html', { 'form': form })

@login_required
@permission_required('avaliacao.delete_avaliacao', raise_exception=True)
def delete(request, id_avaliacao):

    Avaliacao.objects.filter(id=id_avaliacao).delete()

    return HttpResponseRedirect('/avaliacao/')


