from django.db import models
from criterio.models import Criterio

class Barema(models.Model):

    criterios = models.ManyToManyField(Criterio, related_name='baremas')
    nota_obtida = models.PositiveIntegerField()


    def __str__(self):
        
        return f"{self.criterios}: {self.nota_obtida}"