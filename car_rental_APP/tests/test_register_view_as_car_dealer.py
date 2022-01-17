import pytest
from django.contrib.auth.models import User


def client():
  client = Client()
  return client


@pytest.mark.django_db
def test_car_dealer_register(client):
  """New car dealer adding test"""
  client.post('/add_car_dealer/', {'username': 'Matt_Damon', 'email': 'matt.damon@mail.com', 'password': 'Test123',
                                   'first_name': 'Matt', 'last_name': 'Damon', 'is_car_dealer': 'True'})

  assert User.objects.count() == 1