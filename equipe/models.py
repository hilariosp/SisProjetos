from django.db import models

class Equipe(models.Model):
    FUNCOES = (
        ('autor', 'Autor'),
        ('orientador', 'Orientador'),
        ('colaborador', 'Colaborador'),
    )
    membro = models.ForeignKey('usuario.Usuario', on_delete=models.CASCADE)
    projeto = models.ForeignKey('projeto.Projeto', on_delete=models.CASCADE)
    funcao = models.CharField(max_length=20, choices=FUNCOES)
    data_entrada = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('membro', 'projeto')
        verbose_name = 'Membro da Equipe'
        verbose_name_plural = 'Membros da Equipe'

    def __str__(self):
        return f'{self.membro.username} - {self.projeto.nome} ({self.funcao})'
