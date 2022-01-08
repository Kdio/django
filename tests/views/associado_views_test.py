import pytest
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from app.models.associado import Associado
from app.models.contrato import Contrato
from app.models.contratacao import Contratacao


def test_associado_index_not_logged_in(client):
    response = client.get(reverse('associado_index'))
    assert response.status_code == 302
    assert 'login' in response['Location']


@pytest.mark.django_db
def test_associado_index_as_user(auto_login_user):
    client, _user = auto_login_user()
    Associado(nome='Teste').save()
    response = client.get(reverse('associado_index'))
    assert response.status_code == 200
    for string in [b'Teste', b'Alterar', b'Excluir']:
        assert string in response.content


@pytest.mark.django_db
def test_associado_show(auto_login_user):
    contrato = Contrato.objects.create(nome=f"Contrato Nome")
    associado = Associado.objects.create(nome=f"Associado Nome")
    contratacao = Contratacao.objects.create(contrato=contrato, associado=associado, descricao='Descrição', valor=1.00, ativa=True)
    client, _user = auto_login_user()
    response = client.get(reverse('associado_show', kwargs={'associado_id':associado.id}))
    assert response.status_code == 200
    for string in [b'Associado Nome', b'Contrato Nome', bytes('Descrição', 'utf-8'), b'Alterar', b'Excluir']:
        assert string in response.content


@pytest.mark.django_db
def test_associado_new(auto_login_user):
    client, _user = auto_login_user()
    response = client.get(reverse('associado_new'))
    assert response.status_code == 200
    response = client.post(
        reverse('associado_new'), data=dict(nome="Associado"), follow=True)
    assert response.status_code == 200
    assert b'Registro criado com sucesso' in response.content
    for string in [b'Associado', b'Alterar', b'Excluir']:
        assert string in response.content


@pytest.mark.django_db
def test_associado_edit(auto_login_user):
    client, _user = auto_login_user()
    associado = create_associado()
    response = client.get(reverse('associado_edit', kwargs={'associado_id':associado.id}))
    assert response.status_code == 200
    response = client.post(
        reverse('associado_edit', kwargs={'associado_id':associado.id}),
        data=dict(nome="Associado"), follow=True)
    assert response.status_code == 200
    assert b'Registro salvo com sucesso' in response.content
    for string in [b'Associado', b'Alterar', b'Excluir']:
        assert string in response.content


@pytest.mark.django_db
def test_associado_delete(auto_login_user):
    client, _user = auto_login_user()
    associado = create_associado()
    response = client.post(reverse('associado_delete'), data=dict(id_=associado.id), follow=True)
    assert response.status_code == 200
    assert bytes('Registro excluído com sucesso', 'utf-8') in response.content
    with pytest.raises(ObjectDoesNotExist):
        Associado.objects.get(id=associado.id)


def create_associado():
    return Associado.objects.create(nome='Teste')
