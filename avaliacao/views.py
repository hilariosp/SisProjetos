from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import transaction
from .models import Avaliacao
from barema.models import Barema
from criterio.models import Criterio
from .forms import AvaliacaoForm


@login_required
def index(request): 
    if request.user.is_superuser:
        avaliacoes = Avaliacao.objects.select_related('projeto', 'avaliador').all()
    else:
        avaliacoes = Avaliacao.objects.filter(avaliador=request.user).select_related('projeto', 'avaliador')
    
    return render(request, 'avaliacao/index.html', {'avaliacoes': avaliacoes.order_by('-data_avaliacao')})

@login_required
def detail(request, id_avaliacao):
    avaliacao = get_object_or_404(Avaliacao, id=id_avaliacao)
    if not request.user.is_superuser and avaliacao.avaliador != request.user:
        messages.error(request, "Você não tem permissão para ver esta avaliação.")
        return redirect('avaliacao:avaliacao_index')
        
    return render(request, 'avaliacao/detail.html', {'avaliacao': avaliacao})

def _processar_formulario_avaliacao(request, instance=None):
    NOTA_MAXIMA_PADRAO = 10  # A nota máxima padrão que usaremos

    if request.method == 'POST':
        form = AvaliacaoForm(request.POST, instance=instance)
        if form.is_valid():
            try:
                with transaction.atomic():
                    avaliacao = form.save(commit=False)
                    if not instance:
                        avaliacao.avaliador = request.user
                    avaliacao.save()

                    todos_criterios = Criterio.objects.all()
                    if not todos_criterios.exists(): # Adicionado para o caso de não haver critérios
                        pass # Permite salvar a avaliação mesmo sem critérios cadastrados
                    
                    for criterio in todos_criterios:
                        nota_str = request.POST.get(f'nota_criterio_{criterio.id}')
                        
                        # A validação agora checa se a nota foi fornecida e se está no intervalo correto
                        if nota_str and nota_str.isdigit():
                            nota = int(nota_str)
                            if not (0 <= nota <= NOTA_MAXIMA_PADRAO):
                                raise ValueError(f"A nota para '{criterio.nome}' deve ser entre 0 e {NOTA_MAXIMA_PADRAO}.")
                            
                            Barema.objects.update_or_create(
                                avaliacao=avaliacao, criterio=criterio, defaults={'nota': nota}
                            )
                        else:
                            # Esta linha causa o erro se o campo não existir no HTML
                            raise ValueError(f"A nota para o critério '{criterio.nome}' é inválida ou não foi fornecida.")
                
                avaliacao.recalcular_e_salvar_nota_final()
                
                success_message = "Avaliação salva com sucesso!"
                messages.success(request, success_message)
                return redirect(reverse('avaliacao:avaliacao_index'))

            except ValueError as e:
                messages.error(request, str(e))
                # Se der erro, recarrega o formulário sem salvar
    else:
        form = AvaliacaoForm(instance=instance)
    
    # Se a requisição for GET ou o formulário for inválido, retorna o form para o template
    return form

@login_required
@permission_required('avaliacao.add_avaliacao', raise_exception=True)
def add(request): 
    form = _processar_formulario_avaliacao(request)
    if not isinstance(form, AvaliacaoForm):
        return form 

    todos_criterios = Criterio.objects.all().order_by('id')
    criterios_com_notas = [{'criterio': c, 'nota_atual': 0} for c in todos_criterios]

    context = {
        'form': form,
        'criterios_com_notas': criterios_com_notas,
        'instance': None
    }
    return render(request, 'avaliacao/add.html', context)

@login_required
@permission_required('avaliacao.change_avaliacao', raise_exception=True)
def update(request, id_avaliacao):
    avaliacao = get_object_or_404(Avaliacao, id=id_avaliacao)
    if not request.user.is_superuser and avaliacao.avaliador != request.user:
        messages.error(request, "Você não tem permissão para editar esta avaliação.")
        return redirect('avaliacao:avaliacao_index')

    form = _processar_formulario_avaliacao(request, instance=avaliacao)
    if not isinstance(form, AvaliacaoForm):
        return form
    
    todos_criterios = Criterio.objects.all().order_by('id')
    criterios_com_notas = []
    for criterio in todos_criterios:
        nota = 0
        barema_existente = avaliacao.barema.filter(criterio=criterio).first()
        if barema_existente:
            nota = barema_existente.nota
        criterios_com_notas.append({'criterio': criterio, 'nota_atual': nota})

    context = {
        'form': form,
        'criterios_com_notas': criterios_com_notas,
        'instance': avaliacao
    }
    return render(request, 'avaliacao/update.html', context)

@login_required
@permission_required('avaliacao.delete_avaliacao', raise_exception=True)
def delete(request, id_avaliacao):
    avaliacao = get_object_or_404(Avaliacao, id=id_avaliacao)
    if not request.user.is_superuser and avaliacao.avaliador != request.user:
        messages.error(request, "Você não tem permissão para excluir esta avaliação.")
        return redirect('avaliacao:avaliacao_index')

    avaliacao.delete()
    messages.success(request, f"Avaliação do projeto '{avaliacao.projeto.nome}' foi excluída.")
    return redirect('avaliacao:avaliacao_index')

