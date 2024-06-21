from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Represents a user in database """

    profile_photo = models.ImageField(null=True, blank=True)
    bio = models.TextField(max_length=148, blank=True)
