import pytest
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from app.models.contrato import Contrato


def test_contrato_index_not_logged_in(client):
    response = client.get(reverse('contrato_index'))
    assert response.status_code == 302
    assert reverse('admin:login') in response['Location']


def test_contrato_index_as_user(auto_login_user):
    client, _user = auto_login_user()
    response = client.get(reverse('contrato_index'))
    assert response.status_code == 302
    assert reverse('admin:login') in response['Location']


@pytest.mark.django_db
def test_contrato_index_as_admin(admin_client):
    Contrato(nome='Teste').save()
    response = admin_client.get(reverse('contrato_index'))
    assert response.status_code == 200
    for string in [b'Teste', b'Alterar', b'Excluir']:
        assert string in response.content


@pytest.mark.django_db
def test_contrato_new(admin_client):
    response = admin_client.get(reverse('contrato_new'))
    assert response.status_code == 200
    response = admin_client.post(
        reverse('contrato_new'), data=dict(nome="Contrato"), follow=True)
    assert response.status_code == 200
    assert b'Registro criado com sucesso' in response.content
    for string in [b'Contrato', b'Alterar', b'Excluir']:
        assert string in response.content


@pytest.mark.django_db
def test_contrato_edit(admin_client):
    contrato = create_contrato()
    response = admin_client.get(reverse('contrato_edit', kwargs={'contrato_id':contrato.id}))
    assert response.status_code == 200
    response = admin_client.post(
        reverse('contrato_edit', kwargs={'contrato_id':contrato.id}),
        data=dict(nome="Contrato"), follow=True)
    assert response.status_code == 200
    assert b'Registro salvo com sucesso' in response.content
    for string in [b'Contrato', b'Alterar', b'Excluir']:
        assert string in response.content


@pytest.mark.django_db
def test_contrato_delete(admin_client):
    contrato = create_contrato()
    response = admin_client.post(reverse('contrato_delete'), data=dict(id_=contrato.id), follow=True)
    assert response.status_code == 200
    assert bytes('Registro excluído com sucesso', 'utf-8') in response.content
    with pytest.raises(ObjectDoesNotExist):
        Contrato.objects.get(id=contrato.id)

def create_contrato():
    contrato = Contrato.objects.create(nome='Teste')
    return contrato
