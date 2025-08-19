from django import forms
from .models import Tag

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'maxlength': 30, 'class': 'form-control p_input'}),
        }