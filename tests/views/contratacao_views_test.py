from datetime import date
import pytest
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from app.models.contrato import Contrato
from app.models.associado import Associado
from app.models.contratacao import Contratacao


def create_contratacao(seed=""):
    contrato = Contrato.objects.create(nome=f"Contrato Nome{seed}")
    associado = Associado.objects.create(nome=f"Associado Nome{seed}")
    contratacao = Contratacao.objects.create(contrato=contrato, associado=associado, descricao='Descrição', valor=1.00, ativa=True)
    return [contrato, associado, contratacao]


@pytest.mark.django_db
def test_contratacao_new(auto_login_user):
    associado = Associado.objects.create(nome="Teste")
    client, _user = auto_login_user()
    response = client.get(reverse('contratacao_new', kwargs={'associado_id':associado.id}))
    assert response.status_code == 200
    contrato = Contrato.objects.create(nome='Teste')
    response = client.post(
        reverse('contratacao_new', kwargs={'associado_id':associado.id}),
        data=dict(contrato=contrato.id, valor=1), follow=True)
    assert response.status_code == 200
    assert b'Registro criado com sucesso' in response.content


@pytest.mark.django_db
def test_contratacao_edit(auto_login_user):
    contrato, _associado, contratacao = create_contratacao()
    client, _user = auto_login_user()
    response = client.get(reverse('contratacao_edit', kwargs={'contratacao_id':contratacao.id}))
    assert response.status_code == 200
    response = client.post(
        reverse('contratacao_edit', kwargs={'contratacao_id':contratacao.id}),
        data=dict(contrato=contrato.id, historico='Teste', valor='2'), follow=True)
    assert response.status_code == 200
    assert b'Registro salvo com sucesso' in response.content


@pytest.mark.django_db
def test_contratacao_delete(admin_client):
    _contrato, _associado, contratacao = create_contratacao()
    response = admin_client.post(
        reverse('contratacao_delete'), data=dict(id_=contratacao.id), follow=True)
    assert response.status_code == 200
    assert bytes('Registro excluído com sucesso', 'utf-8') in response.content
    with pytest.raises(ObjectDoesNotExist):
        Contratacao.objects.get(id=contratacao.id)


# @pytest.mark.django_db
# def test_contratacao_print(auto_login_user):
#     client, _user = auto_login_user()
#     contrato, _associado, contratacao = create_contratacao()
#     response = client.post(reverse('contratacao_index'), data=dict(contrato='all'))
#     response = client.get(reverse('contratacao_print'), follow=True)
#     response = client.post(
#         reverse('contratacao_index'),
#         data=dict(contrato=contrato.id, historico='ric', date_start=date.today(), date_end=date.today()))
#     response = client.get(reverse('contratacao_print'), follow=True)
#     assert response.status_code == 200
#     for string in [b'Movimento de caixa', b'Teste', bytes('Histórico', 'utf-8'), b'TOTAL']:
#         assert string in response.content
