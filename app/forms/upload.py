from django import forms
from django.utils.translation import gettext_lazy as _


class UploadForm(forms.Form):
    file = forms.FileField(label=_("Arquivo"), required=True)
