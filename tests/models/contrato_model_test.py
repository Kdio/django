""" Test Contrato model """

from datetime import date
import pytest
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from app.models.associado import Associado
from app.models.contrato import Contrato
from app.models.contratacao import Contratacao

@pytest.mark.django_db
def test_new_contrato():
    """
    GIVEN a Contrato model
    WHEN a new Contrato is created
    THEN check the nome & tipo fields are defined correctly
    """
    contrato = Contrato(nome="Nome")
    assert contrato.nome == "Nome"
    assert contrato.__repr__() == contrato.nome
    assert contrato.__str__() == contrato.nome
    assert contrato.can_delete()
    assert not contrato.contratacoes.all()


@pytest.mark.django_db
def test_contrato_nome_suplied():
    """
    GIVEN a Contrato model
    WHEN a new Contrato is created without nome
    THEN should raise an error
    """
    with pytest.raises(ValidationError) as e_info:
        Contrato(nome="").full_clean()
    assert str(e_info.value) == "{'nome': ['Este campo não pode estar vazio.']}"


@pytest.mark.django_db
def test_contrato_nome_unique():
    """
    GIVEN a Contrato model
    WHEN a new Contrato is created with an existing nome
    THEN should raise an error
    """
    non_existing = Contrato.objects.create(nome="non-existing")
    with pytest.raises(ValidationError) as e_info:
        Contrato(nome="non-existing").full_clean()
    assert str(e_info.value) == "{'nome': ['Contrato com este Nome já existe.']}"


@pytest.mark.django_db
def test_contrato_contratacoes():
    """
    GIVEN a Contrato model relationship with Lancamento
    """
    associado = Associado.objects.create(nome="Teste")
    contrato = Contrato.objects.create(nome="Teste")
    assert contrato.can_delete()
    assert not contrato.contratacoes.all() == []

    Contratacao.objects.create(contrato=contrato, associado=associado, valor=1.00)
    Contratacao.objects.create(contrato=contrato, associado=associado, valor=2.00)
    assert not contrato.can_delete()
    assert contrato.contratacoes.all().count() == 2


@pytest.mark.django_db
def test_contrato_choices():
    """
    GIVEN a Contrato model relationship with Lancamento
    """
    first = Contrato.objects.create(nome="First")
    last = Contrato.objects.create(nome="Last")
    result = [(first.id, first.nome), (last.id, last.nome)]
    assert Contrato.choices() == result
    result = [("all", "(Todos)"), (first.id, first.nome), (last.id, last.nome)]
    assert Contrato.choices(include_all=True) == result
