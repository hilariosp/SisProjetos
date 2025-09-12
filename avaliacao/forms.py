from django import forms
from .models import Avaliacao
from notacriterio.models import NotaCriterio
from criterio.models import Criterio

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['projeto', 'comentario']
        widgets = {
            'projeto': forms.Select(attrs={'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class NotaCriterioForm(forms.Form):
    criterio_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    nota = forms.IntegerField(min_value=0, max_value=100, required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    comentario_criterio = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))

NotaCriterioFormSet = forms.formset_factory(NotaCriterioForm, extra=0)

class NotaCriterioModelForm(forms.ModelForm):
    class Meta:
        model = NotaCriterio
        fields = ['nota', 'comentario_criterio']
        widgets = {
            'nota': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'comentario_criterio': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

NotaCriterioUpdateFormSet = forms.modelformset_factory(NotaCriterio, form=NotaCriterioModelForm, extra=0)