from django import forms
from .models import Criterio

class CriterioForm(forms.ModelForm):

    class Meta:
        model = Criterio
        fields = ['nome', 'descricao', 'peso']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control p_input'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control p_input', 'rows': 4}),
            'peso': forms.NumberInput(attrs={'class': 'form-control p_input', 'min': 1, 'max': 5, 'value': 1}),
        }
        labels = {
            'nome': 'Nome do Critério',
            'descricao': 'Descrição',
            'peso': 'Peso',
        }
