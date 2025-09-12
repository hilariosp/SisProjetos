from django import forms
from .models import Avaliacao, Projeto


class AvaliacaoForm(forms.ModelForm):

    class Meta:
        model = Avaliacao
        fields = ['projeto', 'comentario']
        widgets = {
            'projeto': forms.Select(attrs={'class': 'form-control p_input'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control p_input', 'rows': 5}),
        }
        labels = {
            'projeto': 'Projeto a ser Avaliado',
            'comentario': 'Feedback Geral',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['projeto'].queryset = Projeto.objects.order_by('nome')