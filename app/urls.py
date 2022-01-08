from django.urls import path

from app.views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', AppLoginView.as_view(), name='login'),
    path('logout/', AppLogoutView.as_view(), name='logout'),
    path('password/', auth.password, name='password'),

    path('associado/', associado.index, name='associado_index'),
    path('associado/index', associado.index, name='associado_index'),
    path('associado/show/<int:associado_id>/', associado.show, name='associado_show'),
    path('associado/new', associado.new, name='associado_new'),
    path('associado/edit/<int:associado_id>/', associado.edit, name='associado_edit'),
    path('associado/delete', associado.delete, name='associado_delete'),

    path('competencia/', competencia.index, name='competencia_index'),
    path('competencia/index', competencia.index, name='competencia_index'),
    path('competencia/new', competencia.new, name='competencia_new'),

    path('contratacao/new/<int:associado_id>/', contratacao.new, name='contratacao_new'),
    path('contratacao/edit/<int:contratacao_id>/', contratacao.edit, name='contratacao_edit'),
    path('contratacao/delete', contratacao.delete, name='contratacao_delete'),

    path('contrato/', contrato.index, name='contrato_index'),
    path('contrato/index', contrato.index, name='contrato_index'),
    path('contrato/new', contrato.new, name='contrato_new'),
    path('contrato/edit/<int:contrato_id>/', contrato.edit, name='contrato_edit'),
    path('contrato/delete', contrato.delete, name='contrato_delete'),

    path('lancamento/', lancamento.index, name='lancamento_index'),
    path('lancamento/index', lancamento.index, name='lancamento_index'),
    path('lancamento/new', lancamento.new, name='lancamento_new'),
    path('lancamento/delete', lancamento.delete, name='lancamento_delete'),
    path('lancamento/print', lancamento.print, name='lancamento_print'),

    path('mensalidade/show/<int:mensalidade_id>/', mensalidade.show, name='mensalidade_show'),
    path('mensalidade/edit/<int:mensalidade_id>/', mensalidade.edit, name='mensalidade_edit'),
    path('mensalidade/pay/<int:mensalidade_id>/', mensalidade.pay, name='mensalidade_pay'),
    path('mensalidade/print/<int:mensalidade_id>/', mensalidade.print, name='mensalidade_print'),
    path('mensalidade/print_associado/<int:associado_id>/', mensalidade.print_associado, name='mensalidade_print_associado'),
    path('mensalidade/print_competencia/<int:competencia_id>/', mensalidade.print_competencia, name='mensalidade_print_competencia'),

    path('rubrica/', rubrica.index, name='rubrica_index'),
    path('rubrica/index', rubrica.index, name='rubrica_index'),
    path('rubrica/new', rubrica.new, name='rubrica_new'),
    path('rubrica/edit/<int:rubrica_id>/', rubrica.edit, name='rubrica_edit'),
    path('rubrica/delete', rubrica.delete, name='rubrica_delete'),

    path('tools/model', tools.model, name='tools_model'),
    path('tools/help', tools.help, name='tools_help'),
    path('tools/backup', tools.backup, name='tools_backup'),
    path('tools/restore', tools.restore, name='tools_restore'),
]
