from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django import forms

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'nome', 'datanasc', 'tipo', 'password1', 'password2']
        labels = {
            'username': 'Nome de Usuário',
            'nome': 'Nome Completo',
            'datanasc': 'Data de Nascimento',
            'tipo': 'Tipo de Usuário',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control p_input'}),
            'nome': forms.TextInput(attrs={'class': 'form-control p_input'}),
            'datanasc': forms.DateInput(attrs={'class': 'form-control p_input', 'type': 'date'}),
            'tipo': forms.Select(attrs={'class': 'form-control p_input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control p_input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control p_input'}),
        }

class UsuarioEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'nome', 'datanasc', 'tipo']
        labels = {
            'username': 'Nome de Usuário',
            'nome': 'Nome Completo',
            'datanasc': 'Data de Nascimento',
            'tipo': 'Tipo de Usuário',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control p_input'}),
            'nome': forms.TextInput(attrs={'class': 'form-control p_input'}),
            'datanasc': forms.DateInput(attrs={'class': 'form-control p_input', 'type': 'date'}),
            'tipo': forms.Select(attrs={'class': 'form-control p_input'}),
        }