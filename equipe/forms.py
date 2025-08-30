from django import forms
from .models import Equipe

class EquipeForm(forms.ModelForm):
    class Meta:
        model = Equipe
        fields = ['nome', 'membros', 'data_entrada']
        widgets = {
            'nome': forms.TextField(attrs={'class': 'form-control'}),
            'membros': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'data_entrada': forms.DateField(attrs={'class': 'form-control'}),
        }