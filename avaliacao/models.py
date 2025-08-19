from django.db import models
from usuario.models import Usuario
from projeto.models import Projeto
from criterio.models import Criterio

class Avaliacao(models.Model):

    avaliador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='avaliacoes_feitas', verbose_name="Avaliador")
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='avaliacoes', verbose_name="Projeto")
    feedback = models.TextField(blank=True, null=True, verbose_name="Feedback")
    data_avaliacao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Avaliação")
    criterios = models.ManyToManyField(Criterio, through='barema.Barema')
    nota_final = models.PositiveIntegerField(default=0, editable=False, verbose_name="Nota Final")

    def recalcular_e_salvar_nota_final(self):

        NOTA_MAXIMA_PADRAO = 10  
        soma_notas_ponderadas = 0
        soma_pesos = 0

        for item_barema in self.barema.all():
            nota_obtida = item_barema.nota
            peso = item_barema.criterio.peso

            if NOTA_MAXIMA_PADRAO > 0:
                nota_normalizada = nota_obtida / NOTA_MAXIMA_PADRAO
                soma_notas_ponderadas += nota_normalizada * peso
                soma_pesos += peso

        if soma_pesos == 0:
            self.nota_final = 0
        else:
            media_final = soma_notas_ponderadas / soma_pesos
            self.nota_final = int(round(media_final * 100))
        
        self.save(update_fields=['nota_final'])

    def __str__(self):
        projeto_nome = self.projeto.nome if self.projeto else "Projeto não definido"
        avaliador_nome = self.avaliador.get_full_name() if self.avaliador else "Avaliador não definido"
        return f"Avaliação de '{projeto_nome}' por {avaliador_nome}"

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"