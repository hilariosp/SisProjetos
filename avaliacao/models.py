from django.db import models
from usuario.models import Usuario
from projeto.models import Projeto
from barema.models import Barema

class Avaliacao(models.Model):

    avaliador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='avaliacoes_feitas', verbose_name="Avaliador")
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='avaliacoes', verbose_name="Projeto")
    barema = models.ForeignKey(Barema, on_delete=models.SET_NULL, null=True, related_name='avaliacoes')
    comentario = models.TextField(blank=True, null=True, verbose_name="Feedback")
    data_avaliacao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Avaliação")
    nota_final = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, verbose_name="Nota Final")

    def __str__(self):
        return f"Avaliação de {self.projeto} por {self.avaliador}"

    def recalcular_e_salvar_nota_final(self):

        from django.db.models import Sum
        soma = self.notas_dos_criterios.aggregate(soma_total=Sum('nota'))['soma_total']
        self.nota_final = soma if soma is not None else 0
        self.save()
