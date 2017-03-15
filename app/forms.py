from django import forms
from .models import Tabela, Campo, Documento


class TableForm(forms.ModelForm):
    class Meta:
        model = Tabela
        fields = ['nome', 'documento']
        labels = {'nome': 'Nome', 'documento': 'Documento'}


class FieldForm(forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['nome']
        labels = {'nome': 'Campo'}
        widgets = {'ordem': forms.HiddenInput}


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['nome']
        labels = {'nome': 'Documento'}