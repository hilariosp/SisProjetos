from django.db import models
from django.conf import settings

class Equipe(models.Model):
    nome = models.CharField(max_length=100)

    membros = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='MembroEquipe',
        related_name='equipes'
    )

    def __str__(self):
        return self.nome

class MembroEquipe(models.Model):

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE)
    data_entrada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.equipe.nome}"
