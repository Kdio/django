import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_home_not_logged_in(client):
    response = client.get(reverse('home'))
    assert response.status_code == 302
    assert 'login' in response['Location']


@pytest.mark.django_db
def test_home_as_user(auto_login_user):
    client, _user = auto_login_user()
    response = client.post(reverse('home'))
    assert response.status_code == 200
