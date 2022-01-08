from django import forms
from app.models.contrato import Contrato

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['nome']
        widgets = { 'nome': forms.TextInput(attrs={'class': 'form-control'}) }
