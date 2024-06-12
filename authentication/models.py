from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_photo = models.ImageField(null=True, blank=True)


class UserFollows(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'followed_user')
