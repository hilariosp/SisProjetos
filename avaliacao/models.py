from django.db import models
from usuario.models import Usuario
from projeto.models import Projeto

class Avaliacao(models.Model):

    avaliador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='avaliacoes_feitas', verbose_name="Avaliador")
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='avaliacoes', verbose_name="Projeto")
    comentario = models.TextField(blank=True, null=True, verbose_name="Feedback")
    data_avaliacao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Avaliação")

    def __str__(self):
        return f"{self.avaliador}: {self.projeto}"
