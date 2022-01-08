""" Test Alinea model """

from datetime import date
import pytest
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from app.models.alinea import Alinea
from app.models.mensalidade import Mensalidade
from app.models.contrato import Contrato
from app.models.contratacao import Contratacao
from app.models.competencia import Competencia
from app.models.associado import Associado


@pytest.mark.django_db
def test_new_alinea():
    """
    GIVEN a Alinea model
    WHEN a new Alinea is created
    THEN check the nome & tipo fields are defined correctly
    """
    associado=Associado(nome='Associado')
    alinea = Alinea(
        mensalidade=Mensalidade(
            competencia=Competencia(ano="2020", mes="01", data=date.today()),
            associado=associado, data_vence=date.today()),
        contratacao=Contratacao(associado=associado, contrato=Contrato(nome="Contrato"),
            descricao="Desc"), valor=1)
    assert alinea.__repr__() == f'2020/01/Associado/{date.today()}/Associado/Contrato/Desc'
    assert alinea.__str__() == f'2020/01/Associado/{date.today()}/Associado/Contrato/Desc'
    assert not alinea.can_delete()
