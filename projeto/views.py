from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Projeto
from .forms import ProjetoForm
from usuario.models import Usuario
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('projeto.view_projeto', raise_exception=True)
def index(request): 

    Projetos = Projeto.objects.all()
    return render(request, 'projeto/index.html', {'projetos': Projetos})

@login_required
@permission_required('projeto.view_projeto', raise_exception=True)
def detail(request, id_projeto):
    projeto_obj = Projeto.objects.get(id=id_projeto)
    return render(request, 'projeto/detail.html', {'projeto': projeto_obj})

@login_required
@permission_required('projeto.add_projeto', raise_exception=True)
def add(request):
    if request.method == 'POST':
        form = ProjetoForm(request.POST)
        if form.is_valid():
            projeto_instance = form.save(commit=False)
            projeto_instance.autor = Usuario.objects.get(id=request.user.id)
            projeto_instance.save()            
            form.save_m2m()            
            return redirect('projeto:projeto_index')
    else:
        form = ProjetoForm()

    return render(request, 'projeto/add.html', {'form': form})

@login_required
@permission_required('projeto.change_projeto', raise_exception=True)
def update(request, id_projeto):
    projeto = Projeto.objects.get(id=id_projeto)

    if request.method == 'POST':
        form = ProjetoForm(request.POST, instance=projeto)
        if form.is_valid():

            projeto_salvo = form.save()

            tags_selecionadas = form.cleaned_data.get('tags')
            projeto_salvo.tags.set(tags_selecionadas)
            return HttpResponseRedirect('/projeto/')

    else:
        form = ProjetoForm(instance=projeto)

    return render(request, 'projeto/update.html', {'form': form})


@login_required
@permission_required('projeto.delete_projeto', raise_exception=True)
def delete(request, id_projeto):  

    Projeto.objects.filter(id=id_projeto).delete()

    return HttpResponseRedirect('/projeto/')