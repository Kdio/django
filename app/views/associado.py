from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models.associado import Associado
from app.forms.associado import AssociadoForm
from app.utils.public import set_td, set_action, link_to, yes_or_no, date_to_str

@login_required
def index(request):
    associados = Associado.objects.all()
    table_headers = [set_td(_('Nome')),
        set_td(_('Matrícula'), 'c'), set_td(_('Telefone'), 'c'), set_td('action')]
    table_data = []
    table_actions = []
    for associado in associados:
        table_data.append([
            set_td(link_to(reverse('associado_show', kwargs={'associado_id':associado.id}),
                associado.nome)),
            set_td(associado.matricula, 'c'),
            set_td(associado.telefone, 'c')])
        actions = [set_action('edit',
            [reverse('associado_edit', kwargs={'associado_id':associado.id})])]
        if associado.can_delete():
            actions.append(set_action('delete', [associado.id, reverse('associado_delete')]))
        table_actions.append(actions)
    context = {
        'title': _('Associados'),
        'table_headers': table_headers,
        'table_data': table_data,
        'table_actions': table_actions}
    return render(request, 'associado/index.html', context)


@login_required
def show(request, associado_id):
    associado = get_object_or_404(Associado, pk=associado_id)
    contratacoes = table_contratacoes(associado)
    mensalidades = table_mensalidades(associado, request)
    context = {
        'title': _("Associado"), 'associado': associado, 'contratacoes': contratacoes,
        'mensalidades': mensalidades}
    return render(request, 'associado/show.html', context)


@login_required
def new(request):
    form = AssociadoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _("Registro criado com sucesso"))
        return redirect('associado_index')
    context = {'title': _("Novo associado"), 'form': form}
    return render(request, 'associado/form.html', context)


@login_required
def edit(request, associado_id):
    associado = get_object_or_404(Associado, pk=associado_id)
    form = AssociadoForm(request.POST or None, instance=associado)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, _("Registro salvo com sucesso"))
            return redirect('associado_index')
    context = {'title': _("Alterar associado"), 'form': form}
    return render(request, 'associado/form.html', context)


@login_required
def delete(request):
    associado = get_object_or_404(Associado, pk=request.POST['id_'])
    if associado.can_delete():
        associado.delete()
        messages.success(request, _("Registro excluído com sucesso"))
    return redirect('associado_index')


def table_contratacoes(associado):
    table_headers = [set_td(_('Contrato')),
        set_td(_('Descrição')), set_td(_('Valor'), 'r'), set_td(_('Ativa'), 'c'), set_td('action')]
    table_data = []
    table_actions = []
    for contratacao in associado.contratacoes.all():
        table_data.append(
            [set_td(contratacao.contrato),
            set_td(contratacao.descricao),
            set_td(contratacao.valor, 'r'),
            set_td(yes_or_no(contratacao.ativa), 'c')])
        actions = [set_action('edit',
            [reverse('contratacao_edit', kwargs={'contratacao_id':contratacao.id})])]
        if contratacao.can_delete():
            actions.append(set_action('delete', [contratacao.id, reverse('contratacao_delete')]))
        table_actions.append(actions)
    return {'table_headers':table_headers, 'table_data':table_data, 'table_actions':table_actions}


def table_mensalidades(associado, request):
    table_headers = [set_td(_('Ano/Mês'), 'c'), set_td(_('Total'), 'r'),
        set_td(_('Data Pgto'), 'c'), set_td(_('Valor Pgto'), 'r'), set_td('action')]
    table_data = []
    table_actions = []
    for mensalidade in associado.mensalidades.all():
        table_data.append(
            [set_td(link_to(reverse('mensalidade_show', kwargs={'mensalidade_id':mensalidade.id}), mensalidade.competencia), 'c'),
            set_td(mensalidade.total(), 'r'),
            set_td(date_to_str(mensalidade.data_pgto), 'c'),
            set_td(mensalidade.valor_pgto or '', 'r')])
        actions = [set_action('print',
                [reverse('mensalidade_print', kwargs={'mensalidade_id':mensalidade.id})])]
        # actions = []
        if request.user.is_staff:
            actions.append(set_action('edit',
                [reverse('mensalidade_edit', kwargs={'mensalidade_id':mensalidade.id})]))
        if not mensalidade.valor_pgto:
            actions.append(set_action('pay',
                [reverse('mensalidade_pay', kwargs={'mensalidade_id':mensalidade.id})]))
        table_actions.append(actions)
    return {'table_headers':table_headers, 'table_data':table_data, 'table_actions':table_actions}
