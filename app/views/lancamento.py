from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from app.models.lancamento import Lancamento
from app.forms.lancamento import LancamentoSearchForm, NewLancamentoForm
from app.utils.public import set_td, set_action, str_to_date, date_to_str

def get_args_for_search(request):
    """ Lancamentos """
    lancamentos = Lancamento.objects
    search_form = LancamentoSearchForm(request.POST or None)
    session_form = {}
    searched = False
    rubrica = search_form['rubrica'].data
    date_start = search_form['date_start'].data
    date_end = search_form['date_end'].data
    historico = search_form['historico'].data
    if rubrica == "all":
        searched = True
        session_form['rubrica'] = rubrica
        lancamentos = lancamentos.exclude(rubrica=None)
    elif rubrica and rubrica.isnumeric():
        searched = True
        session_form['rubrica'] = rubrica
        lancamentos = lancamentos.filter(rubrica_id=int(rubrica))
    if date_start:
        searched = True
        session_form['date_start'] = date_start
        lancamentos = lancamentos.filter(data__gte=str_to_date(date_start))
    if date_end:
        searched = True
        session_form['date_end'] = date_end
        lancamentos = lancamentos.filter(data__lte=str_to_date(date_end))
    if historico:
        searched = True
        session_form['historico'] = historico
        lancamentos = lancamentos.filter(historico__contains=historico)
    if searched:
        lancamentos = lancamentos.all()
    else:
        lancamentos = lancamentos.none()
    return [lancamentos, search_form, session_form]

def get_args_for_print(request):
    """ Lancamentos """
    lancamentos = Lancamento.objects
    session_form = request.session.get('lancamentos_search')
    rubrica = session_form.get('rubrica')
    date_start = session_form.get('date_start')
    date_end = session_form.get('date_end')
    historico = session_form.get('historico')
    if rubrica == "all":
        lancamentos = lancamentos.exclude(rubrica=None)
    elif rubrica and rubrica.isnumeric():
        lancamentos = lancamentos.filter(rubrica_id=int(rubrica))
    if date_start:
        lancamentos = lancamentos.filter(data__gte=str_to_date(date_start))
    if date_end:
        lancamentos = lancamentos.filter(data__lte=str_to_date(date_end))
    if historico:
        lancamentos = lancamentos.filter(historico__contains=historico)
    return lancamentos.all()


@login_required
def index(request):
    lancamentos, search_form, session_form = get_args_for_search(request)
    request.session['lancamentos_search'] = session_form
    table_headers = [set_td(_('Data'), 'c'), set_td(_('Rúbrica')),
        set_td(_('Histórico')), set_td(_('Valor'), 'r')]
    if request.user.is_staff: table_headers.append(set_td('action'))
    table_data = []
    table_actions = []
    for lancamento in lancamentos:
        table_data.append([set_td(date_to_str(lancamento.data), 'c'), set_td(lancamento.rubrica),
            set_td(lancamento.historico), set_td(lancamento.valor, 'r')])
        if request.user.is_staff:
            table_actions.append([set_action('delete',
                [lancamento.id, reverse('lancamento_delete')])])
    context = {
        'title': _('Lançamentos'),
        'table_headers': table_headers,
        'table_data': table_data,
        'table_actions': table_actions,
        'search_form': search_form,
        'search_form_show': len(table_data) == 0}
    return render(request, 'lancamento/index.html', context)


@login_required
def new(request):
    form = NewLancamentoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _("Registro criado com sucesso"))
        return redirect('lancamento_index')
    context = {'title': _("Novo lançamento"), 'form': form}
    return render(request, 'lancamento/form.html', context)

@staff_member_required
def delete(request):
    lancamento = get_object_or_404(Lancamento, pk=request.POST['id_'])
    if lancamento.can_delete():
        lancamento.delete()
        messages.success(request, _("Registro excluído com sucesso"))
    return redirect('lancamento_index')


@login_required
def print(request):
    lancamentos = get_args_for_print(request)
    table_headers = [set_td(_('Data'), 'c'), set_td(_('Rúbrica')), set_td(_('Histórico')),
        set_td(_('Valor'), 'r')]
    table_data = []
    total = 0
    for lancamento in lancamentos:
        total += lancamento.valor
        table_data.append([set_td(lancamento.data, 'c'), set_td(lancamento.rubrica),
            set_td(lancamento.historico), set_td(lancamento.valor, 'r')])
    table_data.append([set_td(''), set_td(''), set_td('TOTAL'), set_td(total, 'r')])
    context = {
        'title': _('Movimento de caixa'),
        'table_headers': table_headers,
        'table_data': table_data,
        'has_total': True}
    return render(request, 'lancamento/print.html', context)
