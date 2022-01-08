""" Test Associado model """

import pytest
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from app.models.associado import Associado
from app.models.contrato import Contrato
from app.models.contratacao import Contratacao

@pytest.mark.django_db
def test_new_associado():
    """
    GIVEN a Associado model
    WHEN a new Associado is created
    THEN check the nome & tipo fields are defined correctly
    """
    associado = Associado(nome="Nome")
    assert associado.nome == "Nome"
    assert associado.__repr__() == associado.nome
    assert associado.__str__() == associado.nome
    assert associado.can_delete()
    # assert not associado.contratacoes.all()


@pytest.mark.django_db
def test_associado_nome_suplied():
    """
    GIVEN a Associado model
    WHEN a new Associado is created without nome
    THEN should raise an error
    """
    with pytest.raises(ValidationError) as e_info:
        Associado(nome="").full_clean()
    assert str(e_info.value) == "{'nome': ['Este campo não pode estar vazio.']}"


@pytest.mark.django_db
def test_associado_matricula_unique():
    """
    GIVEN a Associado model
    WHEN a new Associado is created with an existing matricula
    THEN should raise an error
    """
    non_existing = Associado.objects.create(nome="Qq", matricula="123")
    with pytest.raises(ValidationError) as e_info:
        Associado(nome="Qq", matricula="123").full_clean()
    assert str(e_info.value) == "{'matricula': ['Associado com este Matrícula já existe.']}"


@pytest.mark.django_db
def test_associado_contratacoes():
    """
    GIVEN a Associado model relationship with Lancamento
    """
    associado = Associado.objects.create(nome="Teste")
    assert associado.can_delete()
    assert not associado.contratacoes.all() == []

    contrato = Contrato.objects.create(nome="Teste")
    Contratacao.objects.create(contrato=contrato, associado=associado, valor=1.00)
    Contratacao.objects.create(contrato=contrato, associado=associado, valor=2.00)
    assert not contrato.can_delete()
    assert contrato.contratacoes.all().count() == 2
