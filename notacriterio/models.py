from django.db import models

class NotaCriterio(models.Model):

    avaliador = models.ForeignKey('usuario.Usuario', on_delete=models.CASCADE, related_name='notas_criterios')
    avaliacao = models.ForeignKey('avaliacao.Avaliacao', on_delete=models.CASCADE, related_name='notas_criterios')
    criterio = models.ForeignKey('criterio.Criterio', on_delete=models.CASCADE, related_name='notas_criterios')
    nota = models.PositiveIntegerField()
    comentario_criterio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.criterio} de {self.avaliacao}: {self.nota}"