import pytest
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from app.models.rubrica import Rubrica


def test_rubrica_index_not_logged_in(client):
    response = client.get(reverse('rubrica_index'))
    assert response.status_code == 302
    assert reverse('admin:login') in response['Location']


def test_rubrica_index_as_user(auto_login_user):
    client, _user = auto_login_user()
    response = client.get(reverse('rubrica_index'))
    assert response.status_code == 302
    assert reverse('admin:login') in response['Location']


@pytest.mark.django_db
def test_rubrica_index_as_admin(admin_client):
    Rubrica(nome='Teste', tipo=1).save()
    response = admin_client.get(reverse('rubrica_index'))
    assert response.status_code == 200
    for string in [b'Teste', bytes('Crédito', 'utf-8'), b'Alterar', b'Excluir']:
        assert string in response.content


@pytest.mark.django_db
def test_rubrica_new(admin_client):
    response = admin_client.get(reverse('rubrica_new'))
    assert response.status_code == 200
    response = admin_client.post(
        reverse('rubrica_new'), data=dict(nome="Rubrica", tipo='-1'), follow=True)
    assert response.status_code == 200
    assert b'Registro criado com sucesso' in response.content
    for string in [b'Rubrica', bytes('Débito', 'utf-8'), b'Alterar', b'Excluir']:
        assert string in response.content


@pytest.mark.django_db
def test_rubrica_edit(admin_client):
    rubrica = create_rubrica()
    response = admin_client.get(reverse('rubrica_edit', kwargs={'rubrica_id':rubrica.id}))
    assert response.status_code == 200
    response = admin_client.post(
        reverse('rubrica_edit', kwargs={'rubrica_id':rubrica.id}),
        data=dict(nome="Rubrica", tipo='1'), follow=True)
    assert response.status_code == 200
    assert b'Registro salvo com sucesso' in response.content
    for string in [b'Rubrica', bytes('Crédito', 'utf-8'), b'Alterar', b'Excluir']:
        assert string in response.content


@pytest.mark.django_db
def test_rubrica_delete(admin_client):
    rubrica = create_rubrica()
    response = admin_client.post(reverse('rubrica_delete'), data=dict(id_=rubrica.id), follow=True)
    assert response.status_code == 200
    assert bytes('Registro excluído com sucesso', 'utf-8') in response.content
    with pytest.raises(ObjectDoesNotExist):
        Rubrica.objects.get(id=rubrica.id)

def create_rubrica():
    rubrica = Rubrica.objects.create(nome='Teste', tipo=-1)
    rubrica.save()
    return rubrica
