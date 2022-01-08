from datetime import date
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models.associado import Associado
from app.models.contratacao import Contratacao
from app.forms.contratacao import NewContratacaoForm, EditContratacaoForm

@login_required
def new(request, associado_id):
    associado = get_object_or_404(Associado, pk=associado_id)
    form = NewContratacaoForm(request.POST or None, instance=Contratacao(associado=associado))
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _("Registro criado com sucesso"))
        return redirect('associado_show', associado_id=associado_id)
    context = {'title': _("Nova contratacao"), 'form': form, 'associado_id': associado_id}
    return render(request, 'contratacao/form.html', context)


@login_required
def edit(request, contratacao_id):
    contratacao = get_object_or_404(Contratacao, pk=contratacao_id)
    form = EditContratacaoForm(request.POST or None, instance=contratacao)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, _("Registro salvo com sucesso"))
            return redirect('associado_show', associado_id=contratacao.associado_id)
    context = {'title': _("Alterar contratacao"), 'form': form,
        'associado_id': contratacao.associado_id}
    return render(request, 'contratacao/form.html', context)


@login_required
def delete(request):
    contratacao = get_object_or_404(Contratacao, pk=request.POST['id_'])
    if contratacao.can_delete():
        contratacao.delete()
        messages.success(request, _("Registro excluído com sucesso"))
    return redirect('associado_show', associado_id=contratacao.associado_id)
