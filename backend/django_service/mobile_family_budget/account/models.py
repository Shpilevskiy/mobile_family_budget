import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def default_expire_date():
    return timezone.now() + timezone.timedelta(days=10)


class RefLink(models.Model):
    link = models.CharField(max_length=120, unique=True)
    creation_date = models.DateField(default=timezone.now)
    expire_date = models.DateField(default=default_expire_date)
    activation_count = models.PositiveIntegerField(default=3)

    def generate_new_link(self):
        self.link = "{}{}".format(self.id, uuid.uuid4().hex)
        self.save()

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
        on_delete=models.CASCADE, unique=True, null=True)

    users = models.ManyToManyField(User)

    name = models.CharField(max_length=30)

    objects = BudgetGroupManager()

    def create_ref_link(self, **kwargs):
        """
        Creates new invite link for the group,
        deletes old link, if exist
        """
        if self.invite_link:
            self.invite_link.delete()

        self.invite_link = RefLink.objects.create(**{k: v for k, v in kwargs.items() if v is not None})
        self.save()
        self.invite_link.generate_new_link()

    def is_member(self, user):
        """
        Returns whether the given user instance
        is the member of the current group
        """
        return self.users.filter(id=user.id).exists()

    def __str__(self):
        return self.name
