from django import forms
from app.models.mensalidade import Mensalidade


class EditMensalidadeForm(forms.ModelForm):
    class Meta:
        model = Mensalidade
        fields = ['data_vence', 'multa', 'saldo','data_pgto', 'valor_pgto']
        widgets = {
            'data_vence': forms.DateTimeInput(
                format='%Y-%m-%d', attrs={'type':'date', 'class': 'form-control'}),
            'multa': forms.NumberInput(attrs={'class': 'form-control text-right currency'}),
            'saldo': forms.NumberInput(attrs={'class': 'form-control text-right currency'}),
            'data_pgto': forms.DateTimeInput(
                format='%Y-%m-%d', attrs={'type':'date', 'class': 'form-control'}),
            'valor_pgto': forms.NumberInput(attrs={'class': 'form-control text-right currency'}),
        }


class PayMensalidadeForm(forms.ModelForm):
    class Meta:
        model = Mensalidade
        fields = ['data_pgto', 'valor_pgto']
        widgets = {
            'data_pgto': forms.DateTimeInput(
                format='%Y-%m-%d', attrs={'type':'date', 'class': 'form-control'}),
            'valor_pgto': forms.NumberInput(attrs={'class': 'form-control text-right currency'}),
        }
