from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag(name='menus_array')
def menus_array():
  return [
    {
      'name': 'Cadastros', 'icon': CADASTRO, 'admin': False, 'options': [
        { 'name': 'Associados', 'icon': ASSOCIADO, 'route': reverse('associado_index'),
          'admin': False },
        { 'name': 'Contratos', 'icon': CONTRATO, 'route': reverse('contrato_index'),
          'admin': True },
        { 'name': 'Competências', 'icon': COMPETENCIA, 'route': reverse('competencia_index'),
          'admin': True }
      ]
    },
    {
      'name': 'Contabilidade', 'icon': CONTABILIDADE, 'admin': False, 'options': [
        { 'name': 'Rúbricas', 'icon': RUBRICA, 'route': reverse('rubrica_index'), 'admin': True },
        { 'name': 'Livro Caixa', 'icon': CAIXA, 'route': reverse('lancamento_index'),
          'admin': False },
      ]
    },
    {
      'name': 'Manutenção', 'icon': MANUTENCAO, 'admin': False, 'options': [
        { 'name': 'Backup', 'icon': BACKUP, 'route': reverse('tools_backup'), 'admin': False },
        { 'name': 'Restaurar', 'icon': RESTORE, 'route': reverse('tools_restore'), 'admin': True },
        { 'name': '-', 'icon': '', 'route': '', 'admin': True },
        { 'name': 'Modelo de dados', 'icon': MODELO, 'route': reverse('tools_model'),
          'admin': False },
        { 'name': 'Ajuda', 'icon': HELP, 'route': reverse('tools_help'), 'admin': False },
      ]
    },
    {
      'name': 'Usuário', 'icon': USUARIO, 'admin': False, 'options': [
        { 'name': 'Alterar senha', 'icon': PASSWORD, 'route': reverse('password'), 'admin': False },
        { 'name': 'Sair', 'icon': SIGNOUT, 'route': reverse('logout'), 'admin': False }
      ]
    }
  ]


CADASTRO = 'fas fa-database'
ASSOCIADO = 'fas fa-user-friends'
CONTRATO = 'far fa-handshake'
COMPETENCIA = 'far fa-calendar-check'
USUARIO = 'fas fa-user'
MENSALIDADE = 'far fa-calendar-alt'

CONTABILIDADE = 'fas fa-dollar-sign'
RUBRICA = 'fas fa-money-check-alt'
CAIXA = 'fas fa-book'
IMPRESSAO = 'fas fas fa-print'

MANUTENCAO = 'fas fa-tools'
BACKUP = 'fas fa-download'
RESTORE = 'fas fa-upload'
MODELO = 'far fa-image'
HELP = 'far fa-question-circle'

PASSWORD = 'fas fa-key'
SIGNOUT = 'fas fa-sign-out-alt'

NEW = 'fas fa-plus-circle'
EDIT = 'far fa-edit'
REMOVE = 'fas fa-trash-alt'
PAY = 'fas fa-hand-holding-usd'
PRINT = 'fas fa-print'
BACK = 'fas fa-arrow-circle-left'
SEARCH = 'fas fa-search'

SUCCESS = 'far fa-check-circle'

CHECK = 'fas fa-check'
UNCHECK = 'fas fa-times'
