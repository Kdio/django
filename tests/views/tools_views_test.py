import os
import pytest
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist


def test_backup_as_user(auto_login_user):
    client, _user = auto_login_user()
    response = client.get(reverse('tools_backup'))
    assert response.status_code == 200
    response = client.post(reverse('tools_backup'))
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == f'inline; filename={os.path.basename(settings.DATABASE_FILE)}'


def test_model_as_user(auto_login_user):
    client, _user = auto_login_user()
    response = client.get(reverse('tools_model'))
    assert response.status_code == 200
    assert b'Modelo de dados' in response.content


def test_help_as_user(auto_login_user):
    client, _user = auto_login_user()
    response = client.get(reverse('tools_help'))
    assert response.status_code == 200
    assert b'Ajuda do sistema' in response.content
    assert bytes('Controle de versões', 'utf-8') in response.content
