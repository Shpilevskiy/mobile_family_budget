from factory import (
    DjangoModelFactory,
    Faker,
    PostGenerationMethodCall
)

from mobile_family_budget.tests.base import DEFAULT_PASSWORD

from django.contrib.auth.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', 'email', 'first_name')

    username = Faker('user_name')
    email = Faker('email')
    password = PostGenerationMethodCall('set_password', DEFAULT_PASSWORD)
    first_name = Faker('first_name')
