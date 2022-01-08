""" Test Rubrica model """

from datetime import date
import pytest
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from app.models.rubrica import Rubrica
from app.models.lancamento import Lancamento

@pytest.mark.django_db
def test_new_rubrica():
    """
    GIVEN a Rubrica model
    WHEN a new Rubrica is created
    THEN check the nome & tipo fields are defined correctly
    """
    rubrica = Rubrica(nome="Nome", tipo=1)
    assert rubrica.nome == "Nome"
    assert rubrica.tipo == 1
    assert rubrica.__repr__() == rubrica.nome
    assert rubrica.__str__() == rubrica.nome
    assert rubrica.can_delete()
    assert not rubrica.lancamentos.all()


@pytest.mark.django_db
def test_new_rubrica_default_tipo():
    """
    GIVEN a Rubrica model
    WHEN a new Rubrica is created withou tipo
    THEN tipo receives a default value
    """
    rubrica = Rubrica(nome="Nome")
    assert rubrica.tipo == 1


@pytest.mark.django_db
def test_rubrica_nome_suplied():
    """
    GIVEN a Rubrica model
    WHEN a new Rubrica is created without nome
    THEN should raise an error
    """
    with pytest.raises(ValidationError) as e_info:
        Rubrica(nome="").full_clean()
    assert str(e_info.value) == "{'nome': ['Este campo não pode estar vazio.']}"


@pytest.mark.django_db
def test_rubrica_nome_unique():
    """
    GIVEN a Rubrica model
    WHEN a new Rubrica is created with an existing nome
    THEN should raise an error
    """
    non_existing = Rubrica.objects.create(nome="non-existing")
    with pytest.raises(ValidationError) as e_info:
        Rubrica(nome="non-existing").full_clean()
    assert str(e_info.value) == "{'nome': ['Rúbrica com este Nome já existe.']}"


@pytest.mark.django_db
def test_rubrica_tipo_acceptable_values():
    """
    GIVEN a Rubrica model
    WHEN a new Rubrica is created with an tipo non-integer
    THEN should raise an error
    """
    with pytest.raises(ValidationError) as e_info:
        Rubrica(nome="Qq", tipo='x').full_clean()
    assert str(e_info.value) == "{'tipo': ['O valor “x” deve ser inteiro.']}"
    with pytest.raises(ValidationError) as e_info:
        Rubrica(nome="Qq", tipo=0).full_clean()
    assert str(e_info.value) == "{'tipo': ['Valor 0 não é uma opção válida.']}"
    rubrica = Rubrica(nome="Qq", tipo=1)
    rubrica.full_clean()
    assert rubrica.str_tipo() == _('Crédito')
    rubrica.tipo=-1
    rubrica.full_clean()
    assert rubrica.str_tipo() == _('Débito')


@pytest.mark.django_db
def test_rubrica_lancamentos():
    """
    GIVEN a Rubrica model relationship with Lancamento
    """
    rubrica = Rubrica.objects.create(nome="Teste", tipo=1)
    assert rubrica.can_delete()
    assert not rubrica.lancamentos.all() == []

    Lancamento.objects.create(rubrica=rubrica, historico="1", data=date.today(), valor=1.00)
    Lancamento.objects.create(rubrica=rubrica, historico="2", data=date.today(), valor=2.00)
    assert not rubrica.can_delete()
    assert rubrica.lancamentos.all().count() == 2


@pytest.mark.django_db
def test_rubrica_choices():
    """
    GIVEN a Rubrica model relationship with Lancamento
    """
    first = Rubrica.objects.create(nome="First", tipo=1)
    last = Rubrica.objects.create(nome="Last", tipo=1)
    result = [(first.id, first.nome), (last.id, last.nome)]
    assert Rubrica.choices() == result
    result = [("all", "(Todas)"), (first.id, first.nome), (last.id, last.nome)]
    assert Rubrica.choices(include_all=True) == result
