from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from app.models.competencia import Competencia
from app.utils.public import set_td, set_action, date_to_str


@staff_member_required
def index(request):
    competencias = Competencia.objects.all()
    table_headers = [set_td(_('Ano/Mês'), 'c'), set_td(_('Vencimento'), 'c'), set_td('action')]
    table_data = []
    table_actions = []
    for competencia in competencias:
        table_data.append([set_td(competencia, 'c'), set_td(date_to_str(competencia.data), 'c')])
        table_actions.append([set_action('print',
                [reverse('mensalidade_print_competencia', kwargs={'competencia_id':competencia.id})])])
    context = {
        'title': _('Competências'),
        'table_headers': table_headers,
        'table_data': table_data,
        'table_actions': table_actions,
        'table_size': '50%'}
    return render(request, 'competencia/index.html', context)


@staff_member_required
def new(request):
    competencia = Competencia.proxima()
    if request.method == 'POST':
        Competencia.create()
        messages.success(request, _("Registro criado com sucesso"))
        return redirect('competencia_index')
    messages.error(request, _("Muita atenção: esta ação não poderá ser revertida!"))
    context = {'title': _("Abertura de competência"), 'competencia': competencia}
    return render(request, 'competencia/form.html', context)
