from django.db import models

class Equipe(models.Model):

    nome = models.CharField(max_length=100)
    membros = models.ManyToManyField('usuario.Usuario')
    data_entrada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.membros.username}'
