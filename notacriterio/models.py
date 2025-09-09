from django.db import models
from criterio.models import Criterio
from avaliacao.models import Avaliacao

class NotaCriterio(models.Model):
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name="notas_dos_criterios")
    criterio = models.ForeignKey(Criterio, on_delete=models.CASCADE, related_name="notas_recebidas")
    nota = models.PositiveIntegerField()

    class Meta:
        unique_together = ('avaliacao', 'criterio')

    def __str__(self):
        return f"Nota para '{self.criterio.descricao[:20]}...': {self.nota}"