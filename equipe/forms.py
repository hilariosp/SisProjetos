from django import forms
from .models import Equipe

class EquipeForm(forms.ModelForm):
    class Meta:
        model = Equipe
        fields = ['membro', 'projeto', 'funcao']
        widgets = {
            'membro': forms.Select(attrs={'class': 'form-control'}),
            'projeto': forms.Select(attrs={'class': 'form-control'}),
            'funcao': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['membro'].queryset = forms.Usuario.objects.filter(is_active=True).order_by('username')
        self.fields['projeto'].queryset = forms.Projeto.objects.order_by('nome')
        self.fields['membro'].label = "Membro"
        self.fields['projeto'].label = "Projeto"
        self.fields['funcao'].label = "Função na equipe"