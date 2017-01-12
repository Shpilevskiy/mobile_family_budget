from django.db import models
from account.models import BudgetGroup


class PurchaseListManager(models.Manager):
    def participant(self, group_id, purchase_list_id=None):
        budget_group = BudgetGroup.objects.get(id=group_id)
        if purchase_list_id:
            return PurchaseList.objects.filter(id=purchase_list_id, budget_group=budget_group)
        return PurchaseList.objects.filter(budget_group=budget_group)


class PurchaseList(models.Model):
    name = models.CharField(max_length=30, default="Мой список покупок")
    budget_group = models.ForeignKey(BudgetGroup, on_delete=models.CASCADE)

    objects = PurchaseListManager()

    def __str__(self):
        return self.name


class Purchase(models.Model):
    name = models.CharField(max_length=30)
    count = models.IntegerField(default=1)
    price = models.FloatField()
    current_count = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    purchase_list = models.ForeignKey(PurchaseList, on_delete=models.CASCADE)
