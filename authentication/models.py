from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_photo = models.ImageField(null=True, blank=True)


"""class UserFollows(models.Model):
    # Your UserFollows model definition goes here

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', )"""
