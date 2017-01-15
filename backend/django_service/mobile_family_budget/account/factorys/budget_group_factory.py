from factory import (
    DjangoModelFactory,
    Faker,
    SubFactory,
    post_generation
)

from account.models import BudgetGroup

from account.factorys.user_factory import UserFactory
from account.factorys.ref_link_factory import RefLinkFactory


class BudgetGroupFactory(DjangoModelFactory):
    class Meta:
        model = BudgetGroup

        django_get_or_create = ('name', 'group_owner', 'invite_link')

    name = Faker('user_name')
    group_owner = SubFactory(UserFactory)
    invite_link = SubFactory(RefLinkFactory)

    @post_generation
    def users(self, *args, **kwargs):
        self.users.add(self.group_owner)
