import pytest
from django.contrib.auth.models import User


def client():
  client = Client()
  return client


@pytest.mark.django_db
def test_customer_register(client):
  """new customer adding test"""
  client.post('/add_customer/', {'username': 'Katy_Perry', 'email': 'katy.perry@mail.com', 'password': 'tesT123',
                             'first_name': 'Katy', 'last_name': 'Perry', 'is_customer': 'True'})

  assert User.objects.count() == 1