from django.db import models
from django.contrib.auth.models import AbstractUser, Group

class Usuario(AbstractUser):

    TIPOS = (
        ('Aluno', 'Aluno'),
        ('Orientador', 'Orientador'),
        ('Avaliador', 'Avaliador'),
    )


    nome = models.CharField(max_length=100, null=True, blank=True)
    datanasc = models.DateField(null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPOS, blank=True)
    add_em = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.nome} ({self.tipo})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.tipo:
            grupo, created = Group.objects.get_or_create(name=self.tipo)
            self.groups.add(grupo)
