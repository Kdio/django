from django import forms
from app.models.associado import Associado

class AssociadoForm(forms.ModelForm):
    class Meta:
        model = Associado
        fields = ['nome', 'matricula', 'telefone']
        widgets = {
            'nome': forms.TextInput(attrs={'size':30, 'class': 'form-control'}),
            'matricula': forms.TextInput(attrs={'size':10, 'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'size':10, 'class': 'form-control'}),
        }
