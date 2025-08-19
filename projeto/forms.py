from django.forms import ModelForm
from .models import Projeto
from django import forms

class ProjetoForm(ModelForm):

    class Meta:
        model = Projeto
        fields = ['nome', 'introducao', 'resumo', 'referencial_teorico', 'desenvolvimento', 'resultados', 'conclusao', 'referencias']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control p_input'}),
            'introducao': forms.Textarea(attrs={'class': 'form-control p_input', 'rows': 5}),
            'resumo': forms.Textarea(attrs={'class': 'form-control p_input', 'rows': 5}),
            'referencial_teorico': forms.Textarea(attrs={'class': 'form-control p_input', 'rows': 5}),
            'desenvolvimento': forms.Textarea(attrs={'class': 'form-control p_input', 'rows': 5}),
            'resultados': forms.Textarea(attrs={'class': 'form-control p_input', 'rows': 5}),
            'conclusao': forms.Textarea(attrs={'class': 'form-control p_input', 'rows': 5}),
            'referencias': forms.Textarea(attrs={'class': 'form-control p_input', 'rows': 5}),
        }