from factory import (
    DjangoModelFactory,
    sequence,
    SubFactory
)

from purchaseManager.models import PurchaseList

from account.models import BudgetGroup


class PurchasesListFactory(DjangoModelFactory):
    class Meta:
        model = PurchaseList

        django_get_or_create = ('name', 'budget_group')

    name = sequence(lambda n: "purchases list №{}".format(n))
    budget_group = SubFactory(BudgetGroup)
