from django import forms
from .models import Avaliacao
from projeto.models import Projeto
from barema.models import Barema 

class AvaliacaoForm(forms.ModelForm):

    projeto = forms.ModelChoiceField(
        queryset=Projeto.objects.all().order_by('nome'),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        label="Projeto a ser Avaliado"
    )

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

# avaliacao/forms.py

from django import forms
from .models import Avaliacao
from projeto.models import Projeto


class AvaliacaoForm(forms.ModelForm):
    
    projeto = forms.ModelChoiceField(
        queryset=Projeto.objects.all().order_by('nome'),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        label="Projeto a ser Avaliado"
    )

    barema = forms.ModelChoiceField(
        queryset=Barema.objects.all().order_by('nome'),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        label="Barema a ser Utilizado"
    )

    class Meta:
        model = Avaliacao
        fields = ['projeto', 'barema', 'comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Deixe seu feedback sobre o projeto...'}),
        }