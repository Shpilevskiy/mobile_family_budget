from factory import (
    DjangoModelFactory,
    sequence,
    SubFactory,
    LazyAttribute
)

from faker import Faker

from purchaseManager.models import Purchase

from purchaseManager.factorys.purchases_list_factory import PurchasesListFactory

fake = Faker()


class PurchaseFactory(DjangoModelFactory):
    class Meta:
        model = Purchase

        django_get_or_create = ('name', 'count', 'current_count', 'price', 'status', 'purchase_list')

    name = sequence(lambda n: "purchase №{}".format(n))
    count = 1
    current_count = 0
    price = LazyAttribute(lambda x: fake.pyfloat(positive=True, left_digits=3, right_digits=2))
    status = False
    purchase_list = SubFactory(PurchasesListFactory)
