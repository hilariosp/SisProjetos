from django.db import models
from criterio.models import Criterio
from avaliacao.models import Avaliacao

class Barema(models.Model):

    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name='barema')
    criterio = models.ForeignKey(Criterio, on_delete=models.CASCADE)
    nota = models.PositiveIntegerField()

    class Meta:
        unique_together = ('avaliacao', 'criterio')
        verbose_name = "Item de Barema"
        verbose_name_plural = "Itens de Barema"

    def __str__(self):
        return f"{self.criterio.nome}: {self.nota}"