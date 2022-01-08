from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from app.models.mensalidade import Mensalidade
from app.forms.mensalidade import EditMensalidadeForm, PayMensalidadeForm
from app.utils.public import set_td


@login_required
def show(request, mensalidade_id):
    mensalidade = get_object_or_404(Mensalidade, pk=mensalidade_id)
    table_headers = [set_td(_('Contrato')), set_td(_('Descrição')), set_td(_('Valor'), 'r')]
    table_data = []
    table_actions = []
    for alinea in mensalidade.alineas.all():
        table_data.append(
            [set_td(alinea.contratacao.contrato),
            set_td(alinea.contratacao.descricao),
            set_td(alinea.valor, 'r')])
    context = {
        'title': _('Mensalidade'),
        'table_headers': table_headers,
        'table_data': table_data,
        'table_actions': table_actions,
        'mensalidade': mensalidade
        }
    return render(request, 'mensalidade/show.html', context)


@staff_member_required
def edit(request, mensalidade_id):
    mensalidade = get_object_or_404(Mensalidade, pk=mensalidade_id)
    form = EditMensalidadeForm(request.POST or None, instance=mensalidade)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, _("Registro salvo com sucesso"))
            return redirect('associado_show', associado_id=mensalidade.associado_id)
    context = {'title': _("Alterar mensalidade"), 'form': form,
        'mensalidade': mensalidade, 'edit': True}
    return render(request, 'mensalidade/form.html', context)


@login_required
def pay(request, mensalidade_id):
    mensalidade = get_object_or_404(Mensalidade, pk=mensalidade_id)
    form = PayMensalidadeForm(request.POST or None, instance=mensalidade)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, _("Registro salvo com sucesso"))
            return redirect('associado_show', associado_id=mensalidade.associado_id)
    context = {'title': _("Receber mensalidade"), 'form': form,
        'mensalidade': mensalidade, 'edit': False}
    return render(request, 'mensalidade/form.html', context)



@login_required
def print(request, mensalidade_id):
    mensalidade = get_object_or_404(Mensalidade, pk=mensalidade_id)
    return do_print(request, [mensalidade])


@login_required
def print_associado(request, associado_id):
    mensalidades = Mensalidade.objects.filter(associado_id=associado_id).all()
    return do_print(request, mensalidades)


@login_required
def print_competencia(request, competencia_id):
    mensalidades = Mensalidade.objects.filter(competencia_id=competencia_id).all()
    return do_print(request, mensalidades)


def do_print(request, mensalidades):
    table_headers = [set_td(_('Contrato')), set_td(_('Descrição')), set_td(_('Valor'), 'r')]
    table_datas = []
    for mensalidade in mensalidades:
        table_data = []
        total = 0
        for alinea in mensalidade.alineas.all():
            total += alinea.valor
            table_data.append([set_td(alinea.contratacao.contrato), set_td(alinea.contratacao.descricao), set_td(alinea.valor, 'r')])
        table_data.append([set_td(''), set_td('TOTAL', 'r'), set_td(total, 'r')])
        table_datas.append(table_data)
    context = {
        'title': '',
        'mensalidades': mensalidades,
        'table_headers': table_headers,
        'table_datas': table_datas,
        'has_total': True}
    return render(request, 'mensalidade/print.html', context)
