from django import forms
from .models import Tabela, Campo, Documento


class TableForm(forms.ModelForm):
    class Meta:
        model = Tabela
        fields = ['name', 'document']
        labels = {'name': 'Nome', 'document': 'Documento'}


class FieldForm(forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['name', 'primary']
        labels = {'name': 'Campo', 'primary': 'Chave Primária'}
        widgets = {'order': forms.HiddenInput}


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['name']
        labels = {'name': 'Documento'}