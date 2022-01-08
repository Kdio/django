from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from app.models.contrato import Contrato
from app.forms.contrato import ContratoForm
from app.utils.public import set_td, set_action

@staff_member_required
def index(request):
    contratos = Contrato.objects.all()
    table_headers = [set_td(_('Nome')), set_td('action')]
    table_data = []
    table_actions = []
    for contrato in contratos:
        table_data.append([set_td(contrato.nome)])
        actions = [set_action('edit',
            [reverse('contrato_edit', kwargs={'contrato_id':contrato.id})])]
        if contrato.can_delete():
            actions.append(set_action('delete', [contrato.id, reverse('contrato_delete')]))
        table_actions.append(actions)
    context = {
        'title': _('Contratos'),
        'table_headers': table_headers,
        'table_data': table_data,
        'table_actions': table_actions}
    return render(request, 'contrato/index.html', context)


@staff_member_required
def new(request):
    form = ContratoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _("Registro criado com sucesso"))
        return redirect('contrato_index')
    context = {'title': _("Novo contrato"), 'form': form}
    return render(request, 'contrato/form.html', context)


@staff_member_required
def edit(request, contrato_id):
    contrato = get_object_or_404(Contrato, pk=contrato_id)
    form = ContratoForm(request.POST or None, instance=contrato)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, _("Registro salvo com sucesso"))
            return redirect('contrato_index')
    context = {'title': _("Alterar contrato"), 'form': form}
    return render(request, 'contrato/form.html', context)


@staff_member_required
def delete(request):
    contrato = get_object_or_404(Contrato, pk=request.POST['id_'])
    if contrato.can_delete():
        contrato.delete()
        messages.success(request, _("Registro excluído com sucesso"))
    return redirect('contrato_index')
