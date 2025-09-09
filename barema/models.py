from django.db import models
from criterio.models import Criterio

class Barema(models.Model):

    nome = models.CharField(max_length=60, unique=True, verbose_name="Nome do Barema")
    criterios = models.ManyToManyField(Criterio, related_name="baremas")

    def __str__(self):
        
        return self.nome