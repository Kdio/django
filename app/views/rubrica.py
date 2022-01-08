from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from app.models.rubrica import Rubrica
from app.forms.rubrica import NewRubricaForm, EditRubricaForm
from app.utils.public import set_td, set_action

@staff_member_required
def index(request):
    rubricas = Rubrica.objects.all()
    table_headers = [set_td(_('Nome')), set_td(_('Tipo'), 'c'), set_td('action')]
    table_data = []
    table_actions = []
    for rubrica in rubricas:
        table_data.append([set_td(rubrica.nome), set_td(rubrica.str_tipo(), 'c')])
        actions = [set_action('edit', [reverse('rubrica_edit', kwargs={'rubrica_id':rubrica.id})])]
        if rubrica.can_delete():
            actions.append(set_action('delete', [rubrica.id, reverse('rubrica_delete')]))
        table_actions.append(actions)
    context = {
        'title': _('Rúbricas'),
        'table_headers': table_headers,
        'table_data': table_data,
        'table_actions': table_actions}
    return render(request, 'rubrica/index.html', context)


@staff_member_required
def new(request):
    form = NewRubricaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _("Registro criado com sucesso"))
        return redirect('rubrica_index')
    context = {'title': _("Nova rúbrica"), 'form': form}
    return render(request, 'rubrica/form.html', context)


@staff_member_required
def edit(request, rubrica_id):
    rubrica = get_object_or_404(Rubrica, pk=rubrica_id)
    form = EditRubricaForm(request.POST or None, instance=rubrica)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, _("Registro salvo com sucesso"))
            return redirect('rubrica_index')
    context = {'title': _("Alterar rúbrica"), 'form': form}
    return render(request, 'rubrica/form.html', context)


@staff_member_required
def delete(request):
    rubrica = get_object_or_404(Rubrica, pk=request.POST['id_'])
    if rubrica.can_delete():
        rubrica.delete()
        messages.success(request, _("Registro excluído com sucesso"))
    return redirect('rubrica_index')
