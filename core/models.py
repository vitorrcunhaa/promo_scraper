from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    keywords = models.CharField(max_length=128, blank=True, null=True, default="produto1, produto2")
    instant_searches_left = models.IntegerField(default=3)

