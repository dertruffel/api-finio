import uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.db import models


class NewsObject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guid = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    title_pl = models.CharField(max_length=255, null=True, blank=True)
    link = models.CharField(max_length=255, null=True, blank=True)
    description_pl = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='news', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png'])])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title_eng = models.CharField(max_length=255, null=True, blank=True)
    description_eng = models.TextField(null=True, blank=True)
    translated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type} - {self.title_pl} - {self.guid}"