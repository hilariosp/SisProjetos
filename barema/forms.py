from django import forms
from .models import Barema
from criterio.models import Criterio

class BaremaForm(forms.ModelForm):
    """
    Formulário para criar ou editar um Barema.
    """

    criterios = forms.ModelMultipleChoiceField(
        queryset=Criterio.objects.all().order_by('descricao'),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Critérios de Avaliação"
    )

    class Meta:
        model = Barema
        fields = ['nome', 'criterios']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Barema para TCCs de Engenharia'}),
        }
        labels = {
            'nome': 'Nome do Barema',
        }