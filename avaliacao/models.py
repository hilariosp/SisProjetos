from django.db import models
from usuario.models import Usuario
from projeto.models import Projeto
from barema.models import Barema
from decimal import Decimal

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

        soma_ponderada = Decimal('0.0')
        soma_dos_pesos = 0

        for nota_criterio in self.notas_dos_criterios.select_related('criterio').all():
            nota = Decimal(nota_criterio.nota)
            peso = nota_criterio.criterio.peso
            
            soma_ponderada += nota * peso
            soma_dos_pesos += peso


        if soma_dos_pesos > 0:
            self.nota_final = soma_ponderada / Decimal(soma_dos_pesos)
        else:
            self.nota_final = Decimal('0.0')
            
        self.save()