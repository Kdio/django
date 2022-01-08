""" Test Rubrica model """

from datetime import date
import pytest
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from app.models.rubrica import Rubrica
from app.models.lancamento import Lancamento

@pytest.mark.django_db
def test_new_lancamento():
    """
    """
    rubrica = Rubrica(nome="Nome", tipo=1)
    lancamento = Lancamento(rubrica=rubrica, historico='Histórico', data=date.today(), valor=1.00)
    assert lancamento.rubrica == rubrica
    assert lancamento.tipo() == 1
    assert lancamento.str_tipo() == rubrica.str_tipo()
    assert lancamento.__repr__() == "Nome/Histórico"
    assert lancamento.__str__() == "Nome/Histórico"
    assert lancamento.can_delete()


@pytest.mark.django_db
def test_new_lancamento_set_flag_on_save():
    """
    """
    rubrica_minus = Rubrica.objects.create(nome="Minus", tipo=-1)
    rubrica_plus = Rubrica.objects.create(nome="Plus", tipo=1)
    lancamento = Lancamento(rubrica=rubrica_minus, data=date.today(), valor=1.00)
    assert lancamento.valor == 1.00
    lancamento.save()
    assert lancamento.valor == -1.00
    lancamento.rubrica = rubrica_plus
    lancamento.save()
    assert lancamento.valor == 1.00


@pytest.mark.django_db
def test_lancamento_rubrica_suplied():
    """
    """
    with pytest.raises(ValidationError) as e_info:
        Lancamento(data=date.today(), valor=1.00).full_clean()
    assert str(e_info.value) == "{'rubrica': ['Este campo não pode ser nulo.']}"


@pytest.mark.django_db
def test_lancamento_data_suplied_and_valid():
    """
    """
    rubrica = Rubrica.objects.create(nome="Nome", tipo=1)
    with pytest.raises(ValidationError) as e_info:
        Lancamento(rubrica=rubrica, valor=1.00).full_clean()
    assert str(e_info.value) == "{'data': ['Este campo não pode ser nulo.']}"
    with pytest.raises(ValidationError) as e_info:
        Lancamento(rubrica=rubrica, data="a", valor=1.00).full_clean()
    Lancamento(rubrica=rubrica, data=date.today(), valor=1.00).full_clean()


@pytest.mark.django_db
def test_lancamento_valor_suplied_and_not_zero():
    """
    """
    rubrica = Rubrica.objects.create(nome="Nome", tipo=1)
    with pytest.raises(ValidationError) as e_info:
        Lancamento(rubrica=rubrica, data=date.today()).full_clean()
    assert str(e_info.value) == "{'valor': ['Este campo não pode ser nulo.']}"
    with pytest.raises(ValidationError) as e_info:
        Lancamento(rubrica=rubrica, data=date.today(), valor=0).full_clean()
    assert str(e_info.value) == "{'valor': ['Este campo não pode ser zero.']}"
    Lancamento(rubrica=rubrica, data=date.today(), valor=1.00).full_clean()
