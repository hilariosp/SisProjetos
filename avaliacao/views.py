from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Avaliacao
from notacriterio.models import NotaCriterio
from criterio.models import Criterio
from .forms import AvaliacaoForm, NotaCriterioFormSet, NotaCriterioUpdateFormSet
from django.forms import modelformset_factory
from usuario.models import Usuario
from django.contrib import messages

@login_required
@permission_required('avaliacao.view_avaliacao', raise_exception=True)
def index(request): 
    avaliacoes = Avaliacao.objects.all()
    return render(request, 'avaliacao/index.html', {'avaliacoes': avaliacoes})

@login_required
@permission_required('avaliacao.view_avaliacao', raise_exception=True)
def detail(request, id_avaliacao):
    avaliacao = get_object_or_404(Avaliacao.objects.prefetch_related('notas_criterios__criterio'), pk=id_avaliacao)
    return render(request, 'avaliacao/detail.html', {'avaliacao': avaliacao})

@login_required
@permission_required('avaliacao.add_avaliacao', raise_exception=True)
def add(request):
    if request.user.is_superuser:
        messages.error(request, 'Superusuários não podem adicionar avaliações. Por favor, use uma conta de usuário comum.')
        return redirect('avaliacao:avaliacao_index')
    criterios = Criterio.objects.all()
    initial_data = [{'criterio_id': c.id} for c in criterios]
    
    if request.method == 'POST':
        avaliacao_form = AvaliacaoForm(request.POST)
        formset = NotaCriterioFormSet(request.POST)

        if avaliacao_form.is_valid() and formset.is_valid():
            avaliacao = avaliacao_form.save(commit=False)
            avaliacao.avaliador = Usuario.objects.get(id=request.user.id)
            avaliacao.save()

            for form in formset:
                if form.has_changed() and form.cleaned_data.get('nota') is not None:
                    criterio_id = form.cleaned_data['criterio_id']
                    criterio = get_object_or_404(Criterio, pk=criterio_id)

                    NotaCriterio.objects.create(
                        avaliador=Usuario.objects.get(id=request.user.id),
                        avaliacao=avaliacao,
                        criterio=criterio,
                        nota=form.cleaned_data['nota'],
                        comentario_criterio=form.cleaned_data['comentario_criterio']
                    )

            avaliacao.recalcular_e_salvar_nota_final()
            return redirect('avaliacao:avaliacao_index', id_avaliacao=avaliacao.pk)

    else:
        avaliacao_form = AvaliacaoForm()
        formset = NotaCriterioFormSet(initial=initial_data)
        
    combined_forms = zip(formset, criterios)

    context = {
        'avaliacao_form': avaliacao_form,
        'combined_forms': combined_forms,
        'formset': formset,
    }
    return render(request, 'avaliacao/add.html', context)


@login_required
@permission_required('avaliacao.change_avaliacao', raise_exception=True)
def update(request, id_avaliacao):
    if request.user.is_superuser:
        messages.error(request, 'Superusuários não podem editar avaliações. Por favor, use uma conta de usuário comum.')
        return redirect('avaliacao:avaliacao_index')
    avaliacao = get_object_or_404(Avaliacao.objects.prefetch_related('notas_criterios__criterio'), pk=id_avaliacao)
    
    if request.method == 'POST':
        avaliacao_form = AvaliacaoForm(request.POST, instance=avaliacao)
        formset = NotaCriterioUpdateFormSet(request.POST, queryset=avaliacao.notas_criterios.all())
        
        if avaliacao_form.is_valid() and formset.is_valid():
            avaliacao = avaliacao_form.save()
            formset.save(commit=False)
            
            for nota_criterio in formset.save():
                nota_criterio.save()

            avaliacao.recalcular_e_salvar_nota_final()
            
            return redirect('avaliacao:avaliacao_index', id_avaliacao=avaliacao.pk)
    else:
        avaliacao_form = AvaliacaoForm(instance=avaliacao)
        formset = NotaCriterioUpdateFormSet(queryset=avaliacao.notas_criterios.all())

    combined_forms = zip(formset, avaliacao.notas_criterios.all())

    context = {
        'avaliacao': avaliacao,
        'avaliacao_form': avaliacao_form,
        'combined_forms': combined_forms,
        'formset': formset,
    }
    return render(request, 'avaliacao/update.html', context)

@login_required
@permission_required('avaliacao.delete_avaliacao', raise_exception=True)
def delete(request, id_avaliacao):
    Avaliacao.objects.filter(id=id_avaliacao).delete()
    return redirect('avaliacao:avaliacao_index')