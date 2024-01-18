from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    last_request = models.DateTimeField(null=True, blank=True)
