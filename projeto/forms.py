from django import forms
from .models import Projeto
from tag.models import Tag
from usuario.models import Usuario

class ProjetoForm(forms.ModelForm):

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all().order_by('nome'), 
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Tags"
    )

    membros_selecionados = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.filter(tipo='Aluno').order_by('nome'),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Alunos Membros do Projeto"
    )

    orientador_selecionado = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(tipo='Orientador').order_by('nome'), 
        widget=forms.Select(attrs={'class': 'form-control select2-single', 'data-placeholder': "Selecione um orientador"}), 
        required=False,
        empty_label="Selecione um orientador", 
        label="Orientador do Projeto"
    )

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