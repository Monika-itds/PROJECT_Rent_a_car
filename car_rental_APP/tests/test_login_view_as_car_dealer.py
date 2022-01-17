import pytest
import uuid


def client():
  client = Client()
  return client

"""Password's standard test"""
@pytest.fixture
def test_password():
    return 'strong-password'

"""Login user test"""
@pytest.fixture
def login_user(django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'login' not in kwargs:
            kwargs['login'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)
    return make_user

"""Login user view test"""
@pytest.mark.django_db
def test_view(client):
  response = client.get('/login/')
  assert response.status_code == 200


"""Car dealer login test"""
@pytest.mark.django_db
def test_car_dealer_login(client, create_user, test_password):
  user = create_user()
  url = '/car_dealer_portal/'
  client.post('/login/', {'login': user.username, 'password': test_password})
  response = client.get(url)
  assert response.status_code == 200
