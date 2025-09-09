from django.db import models
from django.contrib.auth.models import User
from equipe.models import Equipe

class Projeto(models.Model):
    nome = models.CharField(max_length=100)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projetos')
    equipe = models.ForeignKey(Equipe, on_delete=models.SET_NULL, null=True, blank=True, related_name='projetos')
    introducao = models.TextField()
    resumo = models.TextField()
    referencial_teorico = models.TextField()
    desenvolvimento = models.TextField()
    resultados = models.TextField()
    conclusao = models.TextField()
    referencias = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('tag.Tag', through='projetotag.ProjetoTag', related_name='projetos')

    def __str__(self):
        return self.nome
    
