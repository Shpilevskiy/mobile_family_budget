from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from datetime import timedelta


class RefLink(models.Model):
    link = models.URLField()
    creation_date = models.DateField(default=timezone.now())
    expire_date = models.DateField(default=timezone.now() + timedelta(days=10))
    activation_count = models.IntegerField(default=5)


class BudgetGroup(models.Model):
    group_owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='+')

    invite_link = models.OneToOneField(
        RefLink,
        on_delete=models.CASCADE)

    users = models.ManyToManyField(User)

    name = models.CharField(max_length=30)
    login = models.CharField(max_length=30, unique=True)