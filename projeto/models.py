from django.db import models

class Projeto(models.Model):
    autor = models.ForeignKey('usuario.Usuario', on_delete=models.CASCADE, related_name='projetos_autorados')
    nome = models.CharField(max_length=200)
    introducao = models.TextField()
    resumo = models.TextField()
    referencial_teorico = models.TextField()
    desenvolvimento = models.TextField()
    resultados = models.TextField()
    conclusao = models.TextField()
    referencias = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

