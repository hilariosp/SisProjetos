from django import forms
from .models import Projeto
from tag.models import Tag
from equipe.models import Equipe

class ProjetoForm(forms.ModelForm):

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all().order_by('nome'), 
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Tags"
    )

    equipe = forms.ModelChoiceField(
        queryset=Equipe.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control p_input'}),
        required=False,
        label="Equipe"
    )
    class Meta:
        model = Projeto
        fields = ['nome', 'introducao', 'resumo', 'referencial_teorico', 'desenvolvimento', 'resultados', 'conclusao', 'referencias', 'equipe', 'tags']        
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