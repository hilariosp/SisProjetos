from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Projeto
from .forms import ProjetoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django import forms

@login_required
def index(request): 

    Projetos = Projeto.objects.all()
    return render(request, 'projeto/index.html', {'projetos': Projetos})

@login_required
def detail(request, id_projeto):
    projeto_obj = Projeto.objects.get(id=id_projeto)
    return render(request, 'projeto/detail.html', {'projeto': projeto_obj})

@login_required
# @permission_required('projeto.add_Projeto', raise_exception=True)
def add(request):
    if request.method == 'POST':
        form = ProjetoForm(request.POST)
        if form.is_valid():
            # 1. Salva o formulário, mas sem salvar as tags ainda (commit=False)
            projeto_instance = form.save(commit=False)
            
            # 2. Atribui o autor corretamente
            projeto_instance.autor = request.user
            
            # 3. Salva a instância principal do projeto no banco
            projeto_instance.save()
            
            # 4. Agora, salva a relação ManyToMany (as tags)
            #    Esta é a linha mais importante!
            form.save_m2m()
            
            return redirect('projeto:projeto_index') # Redireciona para a lista de projetos
    else:
        form = ProjetoForm()
        # Limita a seleção do autor ao usuário logado, se necessário
        form.fields['autor'].initial = request.user
        form.fields['autor'].widget = forms.HiddenInput()


    return render(request, 'projeto/add.html', {'form': form})

@login_required
# @permission_required('projeto.change_Projeto', raise_exception=True)
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
# @permission_required('projeto.delete_projeto', raise_exception=True)
def delete(request, id_projeto):  

    Projeto.objects.filter(id=id_projeto).delete()

    return HttpResponseRedirect('/projeto/')