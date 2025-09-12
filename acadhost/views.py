from django.shortcuts import render
from projeto.models import Projeto  # Importe seu modelo Projeto
from django.db.models import Q # Necessário para a busca por texto

def index(request):
    # Pega os valores da URL, como antes
    query_busca = request.GET.get('q')
    filtro_ordem = request.GET.get('filtro')

    projetos = Projeto.objects.select_related('autor', 'equipe').all()

    # 1. Aplica o filtro de BUSCA por texto 
    if query_busca:
        projetos = projetos.filter(
            Q(nome__icontains=query_busca) |
            Q(resumo__icontains=query_busca) |
            Q(autor__nome__icontains=query_busca) |
            Q(equipe__nome__icontains=query_busca) 

        )

    # 2. Aplica o filtro de ORDENAÇÃO
    if filtro_ordem == 'antiga-publicacao':
        projetos = projetos.order_by('data_criacao')
    elif filtro_ordem == 'a-z':
        projetos = projetos.order_by('nome')
    elif filtro_ordem == 'z-a':
        projetos = projetos.order_by('-nome')
    else:
        # Padrão: Últimas publicações
        projetos = projetos.order_by('-data_criacao')

    # O contexto agora é mais simples, só enviamos os projetos
    context = {
        'projetos': projetos
    }

    return render(request, 'index.html', context)