""" Test Competencia model """

from datetime import date
import pytest
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from app.models.competencia import Competencia
from app.models.mensalidade import Mensalidade
from app.models.associado import Associado
from app.models.alinea import Alinea
from app.models.contrato import Contrato
from app.models.contratacao import Contratacao

@pytest.mark.django_db
def test_new_competencia():
    """
    GIVEN a Competencia model
    WHEN a new Competencia is created
    THEN check the nome & tipo fields are defined correctly
    """
    competencia = Competencia(ano="2022", mes="01", data=date.today())
    assert competencia.ano == "2022"
    assert competencia.mes == "01"
    assert competencia.__repr__() == "2022/01"
    assert competencia.__str__() == "2022/01"
    assert not competencia.can_delete()
    # assert not competencia.mensalidades.all()


@pytest.mark.django_db
def test_competencia_ano_suplied():
    """
    GIVEN a Competencia model
    WHEN a new Competencia is created without ano
    THEN should raise an error
    """
    with pytest.raises(ValidationError) as e_info:
        Competencia(mes="01", data=date.today()).full_clean()
    assert str(e_info.value) == "{'ano': ['Este campo não pode estar vazio.']}"


@pytest.mark.django_db
def test_competencia_mes_suplied():
    """
    GIVEN a Competencia model
    WHEN a new Competencia is created without mes
    THEN should raise an error
    """
    with pytest.raises(ValidationError) as e_info:
        Competencia(ano="2022", data=date.today()).full_clean()
    assert str(e_info.value) == "{'mes': ['Este campo não pode estar vazio.']}"


@pytest.mark.django_db
def test_competencia_data_suplied_and_date():
    """
    GIVEN a Competencia model
    WHEN a new Competencia is created without data
    THEN should raise an error
    """
    with pytest.raises(ValidationError) as e_info:
        Competencia(ano="2022", mes="01").full_clean()
    assert str(e_info.value) == "{'data': ['Este campo não pode ser nulo.']}"
    with pytest.raises(ValidationError) as e_info:
        Competencia(ano="2022", mes="01", data="x").full_clean()


@pytest.mark.django_db
def test_competencia_ano_mes_unique():
    """
    GIVEN a Competencia model
    WHEN a new Competencia is created with an existing ano/mes
    THEN should raise an error
    """
    non_existing = Competencia.objects.create(ano="2022", mes="01", data=date.today())
    with pytest.raises(ValidationError) as e_info:
        Competencia(ano="2022", mes="01", data=date.today()).full_clean()
    assert str(e_info.value) == "{'__all__': ['Competência com este Ano e Mês já existe.']}"
    Competencia(ano="2022", mes="02", data=date.today()).full_clean()


@pytest.mark.django_db
def test_competencia_mensalidades():
    """
    GIVEN a Competencia model relationship with Mensalidade
    """
    competencia = Competencia.objects.create(ano="2022", mes="01", data=date.today())
    assert not competencia.mensalidades.all() == []

    associado = Associado.objects.create(nome="Associado Nome")
    Mensalidade.objects.create(competencia=competencia, associado=associado, data_vence=date.today())
    assert competencia.mensalidades.all().count() == 1


@pytest.mark.django_db
def test_competencia_current():
    """
    GIVEN a Competencia model relationship with Lancamento
    """
    Competencia.objects.create(ano="2022", mes="05", data=date.today())
    Competencia.objects.create(ano="2022", mes="01", data=date.today())
    assert Competencia.current().__str__() == '2022/05'
    Competencia.objects.create(ano="2022", mes="03", data=date.today())
    assert Competencia.current().__str__() == '2022/05'


@pytest.mark.django_db
def test_competencia_proxima():
    """
    GIVEN a Competencia model relationship with Lancamento
    """
    Competencia.objects.create(ano="2022", mes="01", data=date.today())
    assert Competencia.proxima().__str__() == '2022/02'
    Competencia.objects.create(ano="2022", mes="03", data=date.today())
    assert Competencia.proxima().__str__() == '2022/04'


@pytest.mark.django_db
def test_competencia_create():
    """
    GIVEN a Competencia model relationship with Lancamento
    """
    anterior = Competencia.objects.create(ano="2022", mes="12", data=date.today())
    contrato = Contrato.objects.create(nome="Contrato Nome")
    associado = Associado.objects.create(nome="Associado Nome")
    contratacao = Contratacao.objects.create(
        contrato=contrato, associado=associado, descricao='Descrição', valor=1.00, ativa=True)
    Contratacao.objects.create(
        contrato=contrato, associado=associado, descricao='Não', valor=1.00, ativa=False)
    multa = Mensalidade.objects.create(competencia=anterior, associado=associado, data_vence=date.today())
    Alinea.objects.create(mensalidade=multa, contratacao=contratacao, valor=100)
    assert multa.multa is None
    assert Competencia.current() == anterior
    Competencia.create()
    corrente = Competencia.current()
    assert f"{corrente}" == '2023/01'
    multa.refresh_from_db()
    assert multa.multa == 10
    assert associado.contratacoes.count() == 2
    assert corrente.mensalidades.count() == 1
    mensalidade = corrente.mensalidades.all().first()
    assert mensalidade.associado == associado
    assert mensalidade.data_vence == corrente.data
    assert mensalidade.alineas.count() == 1
    alinea = mensalidade.alineas.first()
    assert alinea.contratacao == contratacao
    assert alinea.valor == contratacao.valor
