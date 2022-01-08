from django import forms
from django.utils.translation import gettext_lazy as _
from app.models.rubrica import Rubrica
from app.models.lancamento import Lancamento

class LancamentoSearchForm(forms.Form):
    rubrica = forms.ChoiceField(
        choices=Rubrica.choices(include_all=True),
        label=_('Rúbrica'), required=False,
        initial="",
        widget=forms.Select(attrs={'class': 'form-control form-select'}))
    date_start = forms.DateField(
        label=_('Data início'), required=False,
        widget=forms.DateInput(attrs={'type':'date', 'class': 'form-control'}))
    date_end = forms.DateField(
        label=_('Data fim'), required=False,
        widget=forms.DateInput(attrs={'type':'date', 'class': 'form-control'}))
    historico = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'size':30, 'class': 'form-control'}))


class NewLancamentoForm(forms.ModelForm):
    class Meta:
        model = Lancamento
        fields = ['data', 'rubrica', 'historico', 'valor']
        widgets = {
            'data': forms.DateTimeInput(attrs={'type':'date', 'class': 'form-control'}),
            'rubrica': forms.Select(attrs={'class': 'form-control form-select'}),
            'historico': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control text-right currency'}),
        }
