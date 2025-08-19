from django import forms
from .models import ProjetoTag

class ProjetoTagForm(forms.ModelForm):
    class Meta:
        model = ProjetoTag
        fields = ['projeto', 'tag']
        widgets = {
            'projeto': forms.Select(attrs={'class': 'form-control'}),
            'tag': forms.Select(attrs={'class': 'form-control'}),
        }