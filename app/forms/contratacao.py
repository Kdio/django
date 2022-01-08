from django import forms
from app.models.contratacao import Contratacao

def sim_nao():
    return [('true', 'Sim'),('false', 'Não')]

class NewContratacaoForm(forms.ModelForm):
    class Meta:
        model = Contratacao
        fields = ['contrato', 'descricao', 'valor', 'ativa']
        widgets = {
            'contrato': forms.Select(attrs={'class': 'form-control form-select'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control text-right currency'}),
            'ativa': forms.Select(choices=sim_nao(), attrs={'class': 'form-control form-select'}),
        }

class EditContratacaoForm(forms.ModelForm):
    class Meta:
        model = Contratacao
        fields = ['contrato', 'descricao', 'valor', 'ativa', 'historico']
        widgets = {
            'contrato': forms.Select(
                attrs={'readonly': 'true', 'class': 'form-control form-select'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control text-right currency'}),
            'ativa': forms.Select(choices=sim_nao(), attrs={'class': 'form-control form-select'}),
            'historico': forms.Textarea(attrs={'class': 'form-control'}),
        }
