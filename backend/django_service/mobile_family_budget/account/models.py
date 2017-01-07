from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from datetime import timedelta


class RefLink(models.Model):
    link = models.CharField(max_length=120, unique=True)
    creation_date = models.DateField(default=timezone.now)
    expire_date = models.DateField(default=timezone.now() + timedelta(days=10))
    activation_count = models.PositiveIntegerField(default=3)

    def __str__(self):
        return str(self.link)


class BudgetGroupManager(models.Manager):
    def participant(self, user_id, group_id=None):
        if group_id:
            return BudgetGroup.objects.filter(users__id=user_id, id=group_id)
        return BudgetGroup.objects.filter(users__id=user_id)


class BudgetGroup(models.Model):
    group_owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='+')

    invite_link = models.OneToOneField(
        RefLink,
        on_delete=models.CASCADE, unique=True)

    users = models.ManyToManyField(User)

    name = models.CharField(max_length=30)

    objects = BudgetGroupManager()

    def is_member(self, user):
        """
        Returns whether the given user instance
        is the member of the current group
        """
        return self.users.filter(id=user.id).exists()

    def __str__(self):
        return self.name