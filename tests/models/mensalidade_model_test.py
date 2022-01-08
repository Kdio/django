""" Test Mensalidade model """

import pytest
import decimal
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from app.models.competencia import Competencia
from app.models.associado import Associado
from app.models.mensalidade import Mensalidade
from app.models.alinea import Alinea
from app.models.contratacao import Contratacao
from app.models.contrato import Contrato

def create_mensalidade():
    competencia = Competencia.objects.create(ano="2020", mes="02", data=date.today())
    associado = Associado.objects.create(nome="Nome")
    mensalidade = Mensalidade.objects.create(
        competencia=competencia, associado=associado, data_vence=date.today())
    return [mensalidade, associado, competencia]


def create_mensalidade_full():
    mensalidade, associado, _competencia = create_mensalidade()
    contrato = Contrato.objects.create(nome="Contrato Nome")
    contratacao = Contratacao.objects.create(
        contrato=contrato, associado=associado, descricao='Descrição', valor=1.00, ativa=True)
    Alinea.objects.create(mensalidade=mensalidade, contratacao=contratacao, valor=15)
    contratacao = Contratacao.objects.create(
        contrato=contrato, associado=associado, descricao='Outra', valor=1.00, ativa=True)
    Alinea.objects.create(mensalidade=mensalidade, contratacao=contratacao, valor=15)
    return mensalidade

@pytest.mark.django_db
def test_new_mensalidade():
    """
    """
    competencia = Competencia(ano="2020", mes="02")
    associado = Associado(nome="Nome")
    mensalidade = Mensalidade(competencia=competencia, associado=associado, data_vence=date.today())
    assert mensalidade.competencia == competencia
    assert mensalidade.associado == associado
    assert mensalidade.__repr__() == f"2020/02/Nome/{date.today()}"
    assert mensalidade.__str__() == f"2020/02/Nome/{date.today()}"
    assert not mensalidade.can_delete()


@pytest.mark.django_db
def test_new_mensalidade_associado_competencia_unique():
    """
    """
    mensalidade, associado, competencia = create_mensalidade()
    with pytest.raises(ValidationError) as e_info:
        Mensalidade(competencia=competencia, associado=associado, data_vence=date.today()).full_clean()
    assert str(e_info.value) == "{'__all__': ['Mensalidade com este Associado e Competência já existe.']}"
    associado = Associado.objects.create(nome="Outro")
    Mensalidade(competencia=competencia, associado=associado, data_vence=date.today()).full_clean()


@pytest.mark.django_db
def test_mensalidade_alineas_and_valor():
    """
    """
    mensalidade = create_mensalidade_full()
    assert mensalidade.alineas.all().count() == 2
    assert mensalidade.valor() == 30


@pytest.mark.django_db
def test_mensalidade_juros():
    """
    """
    mensalidade = create_mensalidade_full()
    mensalidade.data_vence = date.today() - timedelta(days=33)
    assert mensalidade.juros() == round(decimal.Decimal(0.3), 2)
    mensalidade.data_pgto = date.today()
    assert mensalidade.juros() == round(decimal.Decimal(0.3), 2)
    # Even when its already paid
    # Zero if data_vence >= today
    mensalidade.data_vence = date.today() + timedelta(days=1)
    assert mensalidade.juros() == 0
    # Zero if data_pgto <= data_vence
    mensalidade.data_vence = date.today() - timedelta(days=1)
    mensalidade.data_pgto = date.today() - timedelta(days=2)
    assert mensalidade.juros() == 0


@pytest.mark.django_db
def test_mensalidade_total():
    """
    """
    mensalidade = create_mensalidade_full()
    mensalidade.data_vence = date.today() - timedelta(days=32)
    assert mensalidade.total() == round(decimal.Decimal(30.3), 2)
    mensalidade.multa = 5
    assert mensalidade.total() == round(decimal.Decimal(35.3), 2)
    mensalidade.saldo = 2
    assert mensalidade.total() == round(decimal.Decimal(33.3), 2)


@pytest.mark.django_db
def test_mensalidade_get_saldo_anterior():
    """
    """
    mensalidade = create_mensalidade_full()
    mensalidade.data_pgto = mensalidade.data_vence
    mensalidade.valor_pgto = mensalidade.total() + 3
    mensalidade.save()
    competencia = Competencia.objects.create(ano="2021", mes="02", data=date.today())
    nova = Mensalidade.objects.create(competencia=competencia, associado=mensalidade.associado, data_vence=date.today())
    assert nova.saldo == 3
