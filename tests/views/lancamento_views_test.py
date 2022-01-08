from datetime import date
import pytest
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from app.models.rubrica import Rubrica
from app.models.lancamento import Lancamento


def create_lancamento():
    rubrica = Rubrica(nome='Teste', tipo=1)
    rubrica.save()
    lancamento = Lancamento(rubrica=rubrica, historico='Histórico', data=date.today(), valor=1.00)
    lancamento.save()
    return [rubrica, lancamento]


def test_lancamento_index_not_logged_in(client):
    response = client.get(reverse('lancamento_index'))
    assert response.status_code == 302
    assert 'login' in response['Location']


def test_lancamento_index_as_user(auto_login_user):
    client, _user = auto_login_user()
    rubrica, lancamento = create_lancamento()
    response = client.post(reverse('lancamento_index'), data=dict(rubrica=rubrica.id))
    assert response.status_code == 200
    for string in [b'Teste', bytes('Histórico', 'utf-8')]:
        assert string in response.content
    assert b'Excluir' not in response.content


@pytest.mark.django_db
def test_lancamento_index_as_admin(admin_client):
    rubrica, lancamento = create_lancamento()
    response = admin_client.post(reverse('lancamento_index'), data=dict(rubrica='all'))
    assert response.status_code == 200
    for string in [b'Teste', bytes('Histórico', 'utf-8'), b'Excluir']:
        assert string in response.content


@pytest.mark.django_db
def test_lancamento_new(auto_login_user):
    client, _user = auto_login_user()
    response = client.get(reverse('lancamento_new'))
    assert response.status_code == 200
    rubrica = Rubrica(nome='Teste', tipo=1)
    rubrica.save()
    response = client.post(
        reverse('lancamento_new'),
        data=dict(rubrica=rubrica.id, data=date.today(), valor=1, historico="Teste"), follow=True)
    assert response.status_code == 200
    assert b'Registro criado com sucesso' in response.content


@pytest.mark.django_db
def test_lancamento_delete(admin_client):
    rubrica, lancamento = create_lancamento()
    response = admin_client.post(
        reverse('lancamento_delete'), data=dict(id_=lancamento.id), follow=True)
    assert response.status_code == 200
    assert bytes('Registro excluído com sucesso', 'utf-8') in response.content
    with pytest.raises(ObjectDoesNotExist):
        Lancamento.objects.get(id=lancamento.id)


@pytest.mark.django_db
def test_lancamento_print(auto_login_user):
    client, _user = auto_login_user()
    rubrica, lancamento = create_lancamento()
    response = client.post(reverse('lancamento_index'), data=dict(rubrica='all'))
    response = client.get(reverse('lancamento_print'), follow=True)
    response = client.post(
        reverse('lancamento_index'),
        data=dict(rubrica=rubrica.id, historico='ric', date_start=date.today(), date_end=date.today()))
    response = client.get(reverse('lancamento_print'), follow=True)
    assert response.status_code == 200
    for string in [b'Movimento de caixa', b'Teste', bytes('Histórico', 'utf-8'), b'TOTAL']:
        assert string in response.content
