from django.db import models
from criterio.models import Criterio

class Barema(models.Model):

    nome = models.CharField(max_length=60, unique=True, verbose_name="Nome do Barema")
    criterio = models.ManyToManyField(Criterio, on_delete=models.CASCADE)
    nota_obtida = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nome}: {self.nota_obtida}"