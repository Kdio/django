import pytest
from datetime import date
from django.utils.translation import gettext_lazy as _
from app.utils.public import *


def test_set_td():
    assert set_td('dado', 'classe') == {'data': 'dado', 'class': 'classe'}
    assert set_td('dado', 'action') == {'data': 'dado', 'class': 'a'}
    assert set_td('action') == {'data': _('Ações'), 'class': 'a'}


def test_set_action():
    assert set_action('action', 'dado') == {'action': "toolbox/actions/action.html", 'data': 'dado'}


def test_str_to_date():
    for test in ['1/1/1', '2/2/2', '2021-01-01', '02-28-2020']:
        assert isinstance(str_to_date(test), date)
    for test in ['x', '13-13', '02-30-2020']:
        assert not str_to_date(test)


def test_yes_or_nothing():
    assert yes_or_nothing(True) == '<i class="icon fas fa-check color-green"></i>'
    assert yes_or_nothing(False) == ""


def test_yes_or_no():
    assert yes_or_no(True) == '<i class="icon fas fa-check color-green"></i>'
    assert yes_or_no(False) == '<i class="icon fas fa-times color-red"></i>'
