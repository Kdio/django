""" Test Contratacao model """

from datetime import date
import pytest
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from app.models.associado import Associado
from app.models.contrato import Contrato
from app.models.contratacao import Contratacao


def create_contratacao(seed=""):
    contrato = Contrato.objects.create(nome=f"Contrato Nome{seed}")
    associado = Associado.objects.create(nome=f"Associado Nome{seed}")
    contratacao = Contratacao.objects.create(contrato=contrato, associado=associado, descricao='Descrição', valor=1.00, ativa=True)
    return [contrato, associado, contratacao]

@pytest.mark.django_db
def test_new_contratacao():
    """
    """
    contrato = Contrato(nome="Contrato Nome")
    associado = Associado(nome="Associado Nome")
    contratacao = Contratacao(contrato=contrato, associado=associado, descricao='Descrição', valor=1.00, ativa=True)
    assert contratacao.contrato == contrato
    assert contratacao.__repr__() == "Associado Nome/Contrato Nome/Descrição"
    assert contratacao.__str__() == "Associado Nome/Contrato Nome/Descrição"
    assert contratacao.can_delete()


@pytest.mark.django_db
def test_contratacao_historico_on_create():
    """
    """
    _x, _y, contratacao = create_contratacao()
    assert contratacao.historico == f"Adicionada em {date.today().strftime('%d/%m/%Y')}"


@pytest.mark.django_db
def test_contratacao_contrato_suplied():
    """
    """
    associado = Associado.objects.create(nome="Associado Nome")
    with pytest.raises(ValidationError) as e_info:
        Contratacao(associado=associado, valor=1).full_clean()
    assert str(e_info.value) == "{'contrato': ['Este campo não pode ser nulo.']}"


@pytest.mark.django_db
def test_contratacao_associado_suplied():
    """
    """
    contrato = Contrato.objects.create(nome="Contrato Nome")
    with pytest.raises(ValidationError) as e_info:
        Contratacao(contrato=contrato, valor=1).full_clean()
    assert str(e_info.value) == "{'associado': ['Este campo não pode ser nulo.']}"


@pytest.mark.django_db
def test_contratacao_valor_suplied():
    """
    """
    _x, _y, contratacao = create_contratacao()
    contratacao.valor = None
    with pytest.raises(ValidationError) as e_info:
        contratacao.full_clean()
    assert str(e_info.value) == "{'valor': ['Este campo não pode ser nulo.']}"


@pytest.mark.django_db
def test_contratacoes_ativas():
    """
    """
    _x, _y, contratacao1 = create_contratacao("1")
    _x, _y, contratacao2 = create_contratacao("2")
    for index, value in enumerate([contratacao1, contratacao2]):
        assert Contratacao.ativas().all()[index] == value
    contratacao2.ativa = False
    contratacao2.save()
    assert Contratacao.ativas().all().count() == 1


@pytest.mark.django_db
def test_contratacoes_associados_ativos():
    """
    """
    _x, _y, contratacao1 = create_contratacao("1")
    _x, _y, contratacao2 = create_contratacao("2")
    assert Contratacao.associados_ativos() == [contratacao1.associado_id, contratacao2.associado_id]
    contratacao2.ativa = False
    contratacao2.save()
    assert Contratacao.associados_ativos() == [contratacao1.associado_id]


@pytest.mark.django_db
def test_contratacoes_ativas_do_associado():
    """
    """
    _x, associado, contratacao1 = create_contratacao("1")
    _x, _y, contratacao2 = create_contratacao("2")
    contratacao2.associado = associado
    contratacao2.save()
    for index, value in enumerate([contratacao1, contratacao2]):
        assert Contratacao.ativas_do_associado(associado.id)[index] == value
    contratacao1.ativa = False
    contratacao1.save()
    assert Contratacao.ativas_do_associado(associado.id).count() == 1
