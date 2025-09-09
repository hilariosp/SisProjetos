from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import transaction
from .models import Avaliacao
from barema.models import Barema
from criterio.models import Criterio
from notacriterio.models import NotaCriterio
from .forms import AvaliacaoForm

@login_required
def index(request): 
    try:
        usuario_avaliador = request.user.usuario
    except Exception:
        usuario_avaliador = None

    if request.user.is_superuser:
        avaliacoes = Avaliacao.objects.select_related('projeto', 'avaliador', 'barema').all()
    elif usuario_avaliador:
        avaliacoes = Avaliacao.objects.filter(avaliador=usuario_avaliador).select_related('projeto', 'avaliador', 'barema')
    else:
        avaliacoes = Avaliacao.objects.none()
    
    return render(request, 'avaliacao/index.html', {'avaliacoes': avaliacoes.order_by('-data_avaliacao')})

@login_required
def detail(request, id_avaliacao):
    avaliacao = get_object_or_404(Avaliacao.objects.prefetch_related('notas_dos_criterios__criterio'), id=id_avaliacao)
    
    if not request.user.is_superuser and hasattr(request.user, 'usuario') and avaliacao.avaliador != request.user.usuario:
        messages.error(request, "Você não tem permissão para ver esta avaliação.")
        return redirect('avaliacao:avaliacao_index')
        
    return render(request, 'avaliacao/detail.html', {'avaliacao': avaliacao})

def _processar_formulario_avaliacao(request, instance=None):
    NOTA_MAXIMA_PADRAO = 10

    if request.method == 'POST':
        form = AvaliacaoForm(request.POST, instance=instance)
        if form.is_valid():
            try:
                with transaction.atomic():
                    avaliacao = form.save(commit=False)
                    if not instance:
                        avaliacao.avaliador = request.user.usuario
                    
                    avaliacao.save()
                    
                    # Limpa notas antigas para garantir consistência na edição
                    avaliacao.notas_dos_criterios.all().delete()
                    
                    # Usa os critérios do barema que foi salvo com a avaliação
                    criterios_do_barema = avaliacao.barema.criterios.all()

                    for criterio in criterios_do_barema:
                        nota_str = request.POST.get(f'nota_criterio_{criterio.id}')
                        
                        if nota_str and nota_str.isdigit():
                            nota = int(nota_str)
                            if not (0 <= nota <= NOTA_MAXIMA_PADRAO):
                                raise ValueError(f"A nota para '{criterio.descricao}' deve ser entre 0 e {NOTA_MAXIMA_PADRAO}.")
                            
                            # Cria a nota na tabela correta (NotaCriterio)
                            NotaCriterio.objects.create(
                                avaliacao=avaliacao, 
                                criterio=criterio, 
                                nota=nota
                            )
                
                if hasattr(avaliacao, 'recalcular_e_salvar_nota_final'):
                    avaliacao.recalcular_e_salvar_nota_final()
                
                messages.success(request, "Avaliação salva com sucesso!")
                return redirect(reverse('avaliacao:avaliacao_index'))

            except Exception as e:
                messages.error(request, str(e))
    else:
        form = AvaliacaoForm(instance=instance)
    
    return form

@login_required
@permission_required('avaliacao.add_avaliacao', raise_exception=True)
def add(request): 
    # A lógica principal de processamento foi movida para a função helper
    form = _processar_formulario_avaliacao(request)
    
    # Se o form foi processado com sucesso (POST), a função helper retorna um Redirect, não o form
    if not isinstance(form, AvaliacaoForm):
        return form 

    # Para a requisição GET, precisamos de todos os baremas para o usuário selecionar
    baremas = Barema.objects.prefetch_related('criterios').all()

    context = {
        'form': form,
        'baremas': baremas, # Passamos todos os baremas para o template
        'instance': None
    }
    return render(request, 'avaliacao/add.html', context)

@login_required
@permission_required('avaliacao.change_avaliacao', raise_exception=True)
def update(request, id_avaliacao):
    avaliacao = get_object_or_404(Avaliacao, id=id_avaliacao)
    
    if not request.user.is_superuser and hasattr(request.user, 'usuario') and avaliacao.avaliador != request.user.usuario:
        messages.error(request, "Você não tem permissão para editar esta avaliação.")
        return redirect('avaliacao:avaliacao_index')

    form = _processar_formulario_avaliacao(request, instance=avaliacao)
    if not isinstance(form, AvaliacaoForm):
        return form
    
    # Carrega os critérios do barema associado a esta avaliação específica
    criterios_do_barema = avaliacao.barema.criterios.all().order_by('id')
    notas_atuais = {nota.criterio_id: nota.nota for nota in avaliacao.notas_dos_criterios.all()}
    
    criterios_com_notas = []
    for criterio in criterios_do_barema:
        criterios_com_notas.append({
            'criterio': criterio, 
            'nota_atual': notas_atuais.get(criterio.id, 0) # Pega a nota existente ou 0
        })

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

    if not request.user.is_superuser and hasattr(request.user, 'usuario') and avaliacao.avaliador != request.user.usuario:
        messages.error(request, "Você não tem permissão para excluir esta avaliação.")
        return redirect('avaliacao:avaliacao_index')

    avaliacao.delete()
    messages.success(request, f"Avaliação do projeto '{avaliacao.projeto.nome}' foi excluída.")
    return redirect('avaliacao:avaliacao_index')