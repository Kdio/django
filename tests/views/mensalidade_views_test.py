import pytest
from datetime import date
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from app.models.mensalidade import Mensalidade
from app.models.competencia import Competencia
from app.models.associado import Associado
from app.models.alinea import Alinea
from app.models.contratacao import Contratacao
from app.models.contrato import Contrato


def create_mensalidade():
    contrato = Contrato.objects.create(nome="Contrato Nome")
    competencia = Competencia.objects.create(ano='2020', mes='01', data=date.today())
    associado = Associado.objects.create(nome="Associado Nome")
    mensalidade = Mensalidade.objects.create(
        competencia=competencia, associado=associado, data_vence=date.today())
    contratacao = Contratacao.objects.create(
        contrato=contrato, associado=associado, descricao='Descrição', valor=1.00, ativa=True)
    Alinea.objects.create(mensalidade=mensalidade, contratacao=contratacao, valor=15)
    return [mensalidade, associado]



@pytest.mark.django_db
def test_mensalidade_show(auto_login_user):
    mensalidade, _ = create_mensalidade()
    client, _user = auto_login_user()
    response = client.get(reverse('mensalidade_show', kwargs={'mensalidade_id':mensalidade.id}))
    assert response.status_code == 200
    for string in [b'Associado Nome', b'Contrato Nome', bytes('Descrição', 'utf-8')]:
        assert string in response.content


@pytest.mark.django_db
def test_mensalidade_edit_user(auto_login_user):
    client, _user = auto_login_user()
    mensalidade, _ = create_mensalidade()
    response = client.get(reverse('mensalidade_edit', kwargs={'mensalidade_id':mensalidade.id}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_mensalidade_edit(admin_client):
    mensalidade, _ = create_mensalidade()
    response = admin_client.get(reverse('mensalidade_edit', kwargs={'mensalidade_id':mensalidade.id}))
    assert response.status_code == 200
    response = admin_client.post(
        reverse('mensalidade_edit', kwargs={'mensalidade_id':mensalidade.id}),
        data=dict(data_vence=f"{date.today()}"), follow=True)
    assert response.status_code == 200
    assert b'Registro salvo com sucesso' in response.content


@pytest.mark.django_db
def test_mensalidade_pay(auto_login_user):
    client, _user = auto_login_user()
    mensalidade, associado = create_mensalidade()
    response = client.get(reverse('associado_show', kwargs={'associado_id':associado.id}))
    assert response.status_code == 200
    assert b'Receber' in response.content
    response = client.get(reverse('mensalidade_pay', kwargs={'mensalidade_id':mensalidade.id}))
    assert response.status_code == 200
    response = client.post(
        reverse('mensalidade_pay', kwargs={'mensalidade_id':mensalidade.id}),
        data=dict(data_pgto=f"{date.today()}", valor_pgto=15), follow=True)
    assert response.status_code == 200
    assert b'Registro salvo com sucesso' in response.content
    assert b'Receber' not in response.content


@pytest.mark.django_db
def test_mensalidade_print(auto_login_user):
    mensalidade, _ = create_mensalidade()
    client, _user = auto_login_user()
    response = client.get(reverse('mensalidade_print', kwargs={'mensalidade_id':mensalidade.id}))
    assert response.status_code == 200
    for string in [b'Associado Nome', b'Contrato Nome', bytes('Descrição', 'utf-8')]:
        assert string in response.content


@pytest.mark.django_db
def test_mensalidade_print_associado(auto_login_user):
    mensalidade, _ = create_mensalidade()
    client, _user = auto_login_user()
    response = client.get(reverse('mensalidade_print_associado', kwargs={'associado_id':mensalidade.associado.id}))
    assert response.status_code == 200
    for string in [b'Associado Nome', b'Contrato Nome', bytes('Descrição', 'utf-8')]:
        assert string in response.content


@pytest.mark.django_db
def test_mensalidade_print_competencia(auto_login_user):
    mensalidade, _ = create_mensalidade()
    client, _user = auto_login_user()
    response = client.get(reverse('mensalidade_print_competencia', kwargs={'competencia_id':mensalidade.competencia.id}))
    assert response.status_code == 200
    for string in [b'Associado Nome', b'Contrato Nome', bytes('Descrição', 'utf-8')]:
        assert string in response.content
