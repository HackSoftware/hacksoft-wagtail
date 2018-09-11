from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    name = models.CharField(_('Name of User'), blank=True, max_length=255)

    def __str__(self):
        return self.username
