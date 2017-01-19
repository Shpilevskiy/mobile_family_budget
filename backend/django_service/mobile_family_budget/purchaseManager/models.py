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


class PurchaseManager(models.Manager):
    def participant(self, purchase_list_id, purchase_id=None):
        purchase_list = PurchaseList.objects.filter(id=purchase_list_id).first()
        if purchase_id:
            return Purchase.objects.filter(id=purchase_id, purchase_list=purchase_list)
        return Purchase.objects.filter(purchase_list_id=purchase_list)


class Purchase(models.Model):
    name = models.CharField(max_length=30)
    count = models.PositiveIntegerField(default=1)
    price = models.FloatField(default=0)
    current_count = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=False)
    purchase_list = models.ForeignKey(PurchaseList, on_delete=models.CASCADE)

    objects = PurchaseManager()

    def __str__(self):
        return self.name
