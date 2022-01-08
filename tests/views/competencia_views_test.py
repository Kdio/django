import pytest
from datetime import date
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from app.models.competencia import Competencia

def create_competencia():
    return Competencia.objects.create(ano='2020', mes='12', data=date.today())


def test_competencia_index_not_logged_in(client):
    response = client.get(reverse('competencia_index'))
    assert response.status_code == 302
    assert reverse('admin:login') in response['Location']


def test_competencia_index_as_user(auto_login_user):
    client, _user = auto_login_user()
    response = client.get(reverse('competencia_index'))
    assert response.status_code == 302
    assert reverse('admin:login') in response['Location']


@pytest.mark.django_db
def test_competencia_index_as_admin(admin_client):
    competencia = create_competencia()
    response = admin_client.get(reverse('competencia_index'))
    assert response.status_code == 200
    for string in [b'2020', b'12']:
        assert string in response.content


@pytest.mark.django_db
def test_competencia_new(admin_client):
    competencia = create_competencia()
    response = admin_client.get(reverse('competencia_new'))
    assert response.status_code == 200
    response = admin_client.post(reverse('competencia_new'), follow=True)
    assert response.status_code == 200
    assert b'Registro criado com sucesso' in response.content
    for string in [b'2021', b'01']:
        assert string in response.content
