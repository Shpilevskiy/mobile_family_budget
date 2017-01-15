from factory import (
    DjangoModelFactory,
    Faker,
    SubFactory,
    RelatedFactory,
    post_generation
)

from account.models import BudgetGroup

from account.factorys.user_factory import UserFactory
from account.factorys.ref_link_factory import RefLinkFactory


class BudgetGroupFactory(DjangoModelFactory):
    class Meta:
        model = BudgetGroup

        django_get_or_create = ('name', 'group_owner')

    name = Faker('user_name')
    group_owner = SubFactory(UserFactory)
    invite_link = RelatedFactory(RefLinkFactory)

    @post_generation
    def users(self, *args, **kwargs):
        self.users.add(self.group_owner)
