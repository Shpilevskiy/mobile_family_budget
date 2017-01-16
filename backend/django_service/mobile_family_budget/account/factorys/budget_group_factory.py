from factory import (
    DjangoModelFactory,
    Faker,
    SubFactory,
    post_generation
)

from account.models import BudgetGroup

from account.factorys.user_factory import UserFactory


class BudgetGroupFactory(DjangoModelFactory):
    class Meta:
        model = BudgetGroup

        django_get_or_create = ('name', 'group_owner')

    name = Faker('user_name')
    group_owner = SubFactory(UserFactory)

    @post_generation
    def users(self, *args, **kwargs):
        self.create_ref_link()
        self.users.add(self.group_owner)
