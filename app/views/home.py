from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    context = {'title': _('Início'), 'conteudo': ''}
    return render(request, 'home.html', context)
