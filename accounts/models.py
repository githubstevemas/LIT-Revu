from django.conf import settings
from django.db import models


class UserFollows(models.Model):
    """ Represents a relation between users in database """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='following',
        on_delete=models.CASCADE
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='followers',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('user', 'followed_user')
        verbose_name = 'User Follow'
        verbose_name_plural = 'User Follows'
