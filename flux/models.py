from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'followed_user')
        verbose_name = 'User Follow'
        verbose_name_plural = 'User Follows'
