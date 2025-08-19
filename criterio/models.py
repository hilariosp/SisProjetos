from django.db import models

class Criterio(models.Model):

    nome = models.CharField(max_length=100, verbose_name="Nome do Critério")
    descricao = models.TextField(verbose_name="Descrição")
    peso = models.PositiveIntegerField(default=1, verbose_name="Peso", help_text="Define a importância deste critério no cálculo da nota final.")

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Critério"
        verbose_name_plural = "Critérios"
