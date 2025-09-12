from django import forms
from django.contrib.auth import get_user_model
from .models import Equipe
from usuario.models import Usuario

class EquipeForm(forms.ModelForm):

    membros = forms.ModelMultipleChoiceField(
            queryset=Usuario.objects.all(), 
            widget=forms.CheckboxSelectMultiple(),
            required=False,
            label="Membros da Equipe"
        )
    
    class Meta:
        model = Equipe
        fields = ['nome', 'membros']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        equipe = super().save(commit=False)
        if commit:
            equipe.save()
            equipe.membros.set(self.cleaned_data['membros'])
        return equipe