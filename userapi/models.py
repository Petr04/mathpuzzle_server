import jwt

from django.db import models

import datetime as dt

from django.conf import settings
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(validators=[validators.validate_email], unique=True, blank=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

    def _generate_jwt_token(self):
        now = dt.datetime.now() 
        exp_dt = now + dt.timedelta(days=30)
        fmtstr = '%d/%m/%Y, %H:%M:%S'

        token = jwt.encode({
            'id': self.pk,
            'exp': exp_dt.timestamp()
        }, settings.SECRET_KEY, algorithm='HS256')

        return token
