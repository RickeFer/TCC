from django import forms
from .models import Table, Field


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['name']
        labels = {'name': 'Nome'}


class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['name', 'primary']
        labels = {'name': 'Campo', 'primary': 'Chave Primária'}
        widgets = {'order': forms.HiddenInput}
