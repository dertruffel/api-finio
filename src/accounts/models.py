import uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from .managers import UserManagerActive, UserManager




class BaseUser(AbstractBaseUser,PermissionsMixin):
    USERNAME_FIELD = 'email'

    password = models.TextField()
    email = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    image = models.TextField(blank=True, null=True)
    last_active = models.DateTimeField(blank=True, null=True)




    def __str__(self):
        return self.email

    class Meta:
        abstract = True
        app_label = 'accounts_base'


class User(
    BaseUser,
    models.Model):
    all_objects = UserManager()
    objects = UserManagerActive()

    date_joined = models.DateTimeField(auto_now_add=True)
    deactivated_at = models.DateTimeField(blank=True, null=True)
    jwt_secret = models.UUIDField(
        default=uuid.uuid4,
        help_text='The field is used by REST framework to create jwt token.',
    )
    display_name = models.CharField(max_length=255, blank=True, null=True)




    class Meta:
        app_label = 'accounts'

    def __str__(self):
        return self.email

    @property
    def model_type(self):
        return 'user'

    def to_json(self):
        if self.is_admin:
            role = 'admin'
        elif self.is_staff:
            role = 'staff'
        else:
            role = 'user'
        return {
            'id': self.id,
            'role': role,
            'email': self.email,
            'display_name': self.display_name,
        }

