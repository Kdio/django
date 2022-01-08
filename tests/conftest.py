""" Tests configuration module """

import pytest


@pytest.fixture
def auto_login_user(client, django_user_model):
  def make_auto_login(user=None):
      user = django_user_model.objects.create_user(username='user', password='password')
      client.force_login(user)
      return client, user
  return make_auto_login
