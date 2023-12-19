import random
import base64

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.crypto import get_random_string

from .fakers import fake

DEFAULT_USER_PASSWORD = 'admin123@'
DEFAULT_ADMIN_EMAIL = 'admin@example.com'
DEFAULT_DISPLAY_NAME = 'administrator'

User = get_user_model()


class Random:
    def __init__(self, choices):
        self.choices = choices

    def __call__(self):
        return random.choice(self.choices)


def override_defaults(default_attrs, overrides):
    """ Function to override default passed attributes and evaluate lazy generation of
    all related instances. """

    result = {}
    for key in default_attrs.keys():
        value = overrides.get(key, default_attrs[key])
        if callable(value):
            value = value()
        result[key] = value
    return result


def populatable(func):
    """ Decorator that adds `population` parameter that can be passed to generator
    to call it multiple times.
    :returns a list of objects if population is specified or single object otherwise. """

    def decorator(**kwargs):
        population = kwargs.pop('population', None)
        if population is None:
            return func(**kwargs)
        return [func(**kwargs) for __ in range(population)]

    return decorator


@populatable
def generate_user(**kwargs) -> User:
    attrs = override_defaults({
        'email': fake.email,
        'is_staff': False,
        'is_superuser': False,
        'password': make_password(DEFAULT_USER_PASSWORD),
        'display_name': DEFAULT_DISPLAY_NAME,
    }, kwargs)
    return User.objects.create(**attrs)



def generate_file():
    return SimpleUploadedFile(
        name='test.pdf',
        content=base64.b64decode(
            'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQ'
            'YV2MwYfj3HwAD0AIyFMd9EgAAAABJRU5ErkJggg=='
        ),
        content_type='application/pdf',
    )


def generate_image():
    return SimpleUploadedFile(
        name='image.gif',
        content=base64.b64decode(
            'R0lGODlhAQABAIABAP8AAP///yH5BAEAAAEALAAAAAABAAEAAAICRAEAOw=='
        ),
        content_type='image/gif',
    )
