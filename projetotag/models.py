from django.db import models

class ProjetoTag(models.Model):
    projeto = models.ForeignKey('projeto.Projeto', on_delete=models.CASCADE)
    tag = models.ForeignKey('tag.Tag', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('projeto', 'tag')
        verbose_name = 'Projeto Tag'
        verbose_name_plural = 'Projetos Tags'

    def __str__(self):
        return f'{self.projeto.nome} + {self.tag.nome}'