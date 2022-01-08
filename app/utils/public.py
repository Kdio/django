""" Public methods """
from dateutil.parser import parse
from django.utils.translation import gettext_lazy as _

def set_td(data, class_=""):
    if data == 'action':
        class_ = data
        data = _('Ações')
    if class_ == 'action':
        class_ = "a"
    return {'data': data, 'class': class_}


def yes_or_nothing(boolean):
    if boolean:
        return '<i class="icon fas fa-check color-green"></i>'
    return ''


def yes_or_no(boolean):
    if boolean:
        return '<i class="icon fas fa-check color-green"></i>'
    return '<i class="icon fas fa-times color-red"></i>'


def set_action(action, data):
    return {'action': f"toolbox/actions/{action}.html", 'data': data}


def link_to(path, caption):
    return f'<a href="{path}">{caption}</a>'


def str_to_date(string, fuzzy=False):
    """ str_to_date method """
    try:
        return parse(string, fuzzy=fuzzy)
    except ValueError:
        return False

def date_to_str(data):
    """ date_to_str method """
    if data:
        return data.strftime('%d/%m/%Y')
    return ''
