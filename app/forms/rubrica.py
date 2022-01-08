from django import forms
from app.models.rubrica import Rubrica

class NewRubricaForm(forms.ModelForm):
    class Meta:
        model = Rubrica
        fields = ['nome', 'tipo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control form-select'})
        }

class EditRubricaForm(forms.ModelForm):
    class Meta:
        model = Rubrica
        fields = ['nome', 'tipo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'readonly': 'true', 'class': 'form-control form-select'})
        }
