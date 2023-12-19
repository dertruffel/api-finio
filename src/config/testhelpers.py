import pytest

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
import websocket


from .generators import generate_user


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return generate_user()



@pytest.fixture
def users():
    return generate_user(population=3)


@pytest.fixture()
def access_token(user):
    return str(AccessToken.for_user(user))


@pytest.fixture()
def refresh_token(user):
    return str(RefreshToken.for_user(user))

@pytest.fixture()
def captcha_settings(settings):
    settings.DRF_RECAPTCHA_TESTING = True
    assert settings.DRF_RECAPTCHA_TESTING is True
    print(f'Captcha settings set to pass,{settings.DRF_RECAPTCHA_TESTING}')
    return settings

@pytest.fixture()
def debug(settings):
    settings.DEBUG = True
    # settings.OMITFEWTHINGS = True
    if settings.DEBUG:
        print('Debug mode enabled')
    # if settings.OMITFEWTHINGS:
    #     print('Omit few things enabled')
    return settings

def authorise_client(client: APIClient, user):
    try:
        user.is_author = True
        user.display_name = 'test'
        user.first_name = 'test'
        user.last_name = 'test'
        user.is_active = True
        user.save()
        access_token = str(AccessToken.for_user(user))
        refresh_token = str(RefreshToken.for_user(user))
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(access_token)}')
        client.user = user
        client.access = access_token
        client.refresh = refresh_token
        print(f'Client authorised ')
        return client
    except Exception as e:
        print(f'Error while authorising client: {e}')
        return client

def get_token(user):
    return str(AccessToken.for_user(user))

@pytest.fixture
def authorised_client(client, user):
    return authorise_client(client, user)

